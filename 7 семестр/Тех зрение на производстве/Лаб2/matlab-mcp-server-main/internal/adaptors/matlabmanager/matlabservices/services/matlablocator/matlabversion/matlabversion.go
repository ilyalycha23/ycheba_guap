// Copyright 2025-2026 The MathWorks, Inc.

package matlabversion

import (
	"encoding/xml"
	"io"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/matlabmanager/matlabservices/customerrors"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/matlabmanager/matlabservices/datatypes"
	"github.com/matlab/matlab-mcp-server/internal/facades/osfacade"
)

type MathWorksVersionInfo struct {
	Release     string `xml:"release"`
	Description string `xml:"description"`
}

var versionResleasePhaseRegexp = regexp.MustCompile(`(?P<phase>[a-zA-Z]*)\s?Update\s?(?P<update>\d+)`)

type OSLayer interface {
	Open(path string) (osfacade.File, error)
}

type IOLayer interface {
	ReadAll(r io.Reader) ([]byte, error)
}

type Getter struct {
	osLayer OSLayer
	ioLayer IOLayer
}

func New(
	osLayer OSLayer,
	ioLayer IOLayer,
) *Getter {
	return &Getter{
		osLayer: osLayer,
		ioLayer: ioLayer,
	}
}

func (s *Getter) Get(matlabRootLocation string) (datatypes.MatlabVersionInfo, error) {
	if matlabRootLocation == "" {
		return datatypes.MatlabVersionInfo{}, customerrors.ErrEmptyLocation
	}

	xmlFilePath := filepath.Join(matlabRootLocation, "VersionInfo.xml")
	xmlFile, err := s.osLayer.Open(xmlFilePath)
	if err != nil {
		return datatypes.MatlabVersionInfo{}, err
	}
	defer xmlFile.Close() //nolint:errcheck // Ignore the error for closing the VersionInfo as it does not impact behaviour

	byteValue, err := s.ioLayer.ReadAll(xmlFile)
	if err != nil {
		return datatypes.MatlabVersionInfo{}, err
	}

	var versionInfo MathWorksVersionInfo
	if err := xml.Unmarshal(byteValue, &versionInfo); err != nil {
		return datatypes.MatlabVersionInfo{}, err
	}

	releasePhase, updateLevel := s.parseReleasePhase(versionInfo.Description)

	return datatypes.MatlabVersionInfo{
		ReleaseFamily: versionInfo.Release,
		ReleasePhase:  releasePhase,
		UpdateLevel:   updateLevel,
	}, nil
}

func (s *Getter) parseReleasePhase(description string) (string, int) {
	match := versionResleasePhaseRegexp.FindStringSubmatch(description)
	result := make(map[string]string)
	if len(match) > 0 {
		for i, value := range match {
			name := versionResleasePhaseRegexp.SubexpNames()[i]
			if i != 0 && name != "" {
				result[name] = value
			}
		}
	}

	var releasePhase string
	if strings.Contains(result["phase"], "Pre") {
		releasePhase = "Prerelease"
	} else {
		releasePhase = "Release"
	}

	updateLevel, err := strconv.Atoi(result["update"])
	if err != nil {
		updateLevel = 0
	}

	return releasePhase, updateLevel
}
