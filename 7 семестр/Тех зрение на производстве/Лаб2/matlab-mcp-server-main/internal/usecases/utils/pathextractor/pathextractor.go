// Copyright 2025 The MathWorks, Inc.

package pathextractor

import (
	"path/filepath"
	"strings"
)

func ExtractPathComponents(absolutePath string) (dir string, filenameWithoutExt string) {
	dir = filepath.Dir(absolutePath)
	filenameWithoutExt = extractFilenameWithoutExt(absolutePath)

	return dir, filenameWithoutExt
}

func extractFilenameWithoutExt(absolutePath string) string {
	baseFilename := filepath.Base(absolutePath)
	return strings.TrimSuffix(baseFilename, filepath.Ext(baseFilename))
}
