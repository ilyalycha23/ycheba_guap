// Copyright 2025-2026 The MathWorks, Inc.

package pathextractor_test

import (
	"path/filepath"
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/usecases/utils/pathextractor"
	"github.com/stretchr/testify/assert"
)

func TestExtractor_ExtractPathComponents(t *testing.T) {
	tests := []struct {
		name                       string
		path                       string
		expectedDir                string
		expectedFilename           string
		expectedFilenameWithoutExt string
	}{
		{
			name:                       "Standard MATLAB file",
			path:                       filepath.Join(".", "folder", "myFunction.m"),
			expectedDir:                filepath.Join(".", "folder"),
			expectedFilename:           "myFunction.m",
			expectedFilenameWithoutExt: "myFunction",
		},
		{
			name:                       "Test file",
			path:                       filepath.Join(".", "folder", "testMyFunction.m"),
			expectedDir:                filepath.Join(".", "folder"),
			expectedFilename:           "testMyFunction.m",
			expectedFilenameWithoutExt: "testMyFunction",
		},
		{
			name:                       "File in current directory",
			path:                       "script.m",
			expectedDir:                ".",
			expectedFilename:           "script.m",
			expectedFilenameWithoutExt: "script",
		},
		{
			name:                       "Complex filename",
			path:                       filepath.Join(".", "deep", "nested", "path", "my_complex.file.name.m"),
			expectedDir:                filepath.Join(".", "deep", "nested", "path"),
			expectedFilename:           "my_complex.file.name.m",
			expectedFilenameWithoutExt: "my_complex.file.name",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Arrange

			// Act
			dir, filenameWithoutExt := pathextractor.ExtractPathComponents(tt.path)

			// Assert
			assert.Equal(t, tt.expectedDir, dir)
			assert.Equal(t, tt.expectedFilenameWithoutExt, filenameWithoutExt)
		})
	}
}
