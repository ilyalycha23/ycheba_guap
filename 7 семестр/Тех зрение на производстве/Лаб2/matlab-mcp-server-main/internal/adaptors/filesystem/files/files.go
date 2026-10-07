// Copyright 2025-2026 The MathWorks, Inc.

package files

import (
	"path/filepath"
	"strings"

	"github.com/matlab/matlab-mcp-server/internal/facades/osfacade"
)

const suffixSeparator = "-"

type OSLayer interface {
	CreateTemp(dir string, pattern string) (osfacade.File, error)
}

type Factory struct {
	osLayer OSLayer
}

func NewFactory(
	osLayer OSLayer,
) *Factory {
	return &Factory{
		osLayer: osLayer,
	}
}

// CreateFileWithUniqueSuffix creates a file, given a base name, with a unique, available suffix.
func (f *Factory) CreateFileWithUniqueSuffix(baseName string, ext string) (string, string, error) {
	fileNameWithStart := f.FilenameWithSuffix(baseName, ext, "*")

	dir := filepath.Dir(fileNameWithStart)
	pattern := filepath.Base(fileNameWithStart)

	tempFile, err := f.osLayer.CreateTemp(dir, pattern)
	if err != nil {
		return "", "", err
	}

	err = tempFile.Close()
	if err != nil {
		return "", "", err
	}

	fileNamWithSuffix := tempFile.Name()

	suffix := getSuffix(baseName, ext, fileNamWithSuffix)

	return fileNamWithSuffix, suffix, nil
}

func (f *Factory) FilenameWithSuffix(baseName string, ext string, suffix string) string {
	// Ensure there is a suffix separator before the suffix
	if !strings.HasSuffix(baseName, suffixSeparator) {
		baseName = baseName + suffixSeparator
	}

	return baseName + suffix + ext
}

func getSuffix(baseName string, ext string, fileNameWithSuffix string) string {
	if !strings.HasSuffix(baseName, suffixSeparator) {
		baseName = baseName + suffixSeparator
	}

	suffix := strings.TrimPrefix(fileNameWithSuffix, baseName)
	suffix = strings.TrimSuffix(suffix, ext)

	return suffix
}
