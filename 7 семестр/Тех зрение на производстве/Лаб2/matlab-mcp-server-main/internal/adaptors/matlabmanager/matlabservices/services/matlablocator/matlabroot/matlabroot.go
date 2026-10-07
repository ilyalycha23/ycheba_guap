// Copyright 2025-2026 The MathWorks, Inc.

package matlabroot

import (
	"errors"
	"os"
	"path/filepath"
	"strings"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/matlabmanager/matlabservices/config"
	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/facades/osfacade"
)

type OSLayer interface {
	Getenv(key string) string
	Stat(name string) (osfacade.FileInfo, error)
}

type FileLayer interface {
	EvalSymlinks(path string) (string, error)
}

type Getter struct {
	osLayer   OSLayer
	fileLayer FileLayer
}

func New(
	osLayer OSLayer,
	fileLayer FileLayer,
) *Getter {
	return &Getter{
		osLayer:   osLayer,
		fileLayer: fileLayer,
	}
}

func (s *Getter) GetAll(logger entities.Logger) []string {
	pathList := strings.Split(s.osLayer.Getenv("PATH"), string(os.PathListSeparator))

	matlabLocations := make([]string, 0)

	for _, path := range pathList {
		// Fix path formatting on all platforms as CMD formatting can be strange
		path = strings.Trim(path, ` "'`)

		if path == "" {
			continue
		}

		path, err := s.fileLayer.EvalSymlinks(path)
		if err != nil {
			logger.With("path", path).WithError(err).Warn("Error evaluating if the path was a symbolic link")
			continue
		}

		matlabExePath := filepath.Join(path, config.MATLABExeName)

		// Check that the MATLAB executable exists and is a file
		fileInfo, err := s.osLayer.Stat(matlabExePath)
		if err != nil {
			if !errors.Is(err, os.ErrNotExist) {
				logger.With("path", matlabExePath).WithError(err).Warn("Unable to evaluate file")
			}
			continue
		}
		if fileInfo.IsDir() {
			continue
		}

		// Follow the executable symlink to find the MATLAB root directory
		// If the executable is not a symlink then the raw path will be the same as the original path
		matlabRawPath, err := s.fileLayer.EvalSymlinks(matlabExePath)
		if err != nil {
			logger.With("path", matlabExePath).WithError(err).Warn("Error evaluating if the found executable was a symbolic link")
			continue
		}

		// The matlab exe is in the bin directory of matlab root and so we need to extract the root directory
		matlabRoot := filepath.Dir(filepath.Dir(matlabRawPath))

		matlabLocations = append(matlabLocations, matlabRoot)
	}

	if len(matlabLocations) == 0 {
		return nil
	}

	return matlabLocations
}
