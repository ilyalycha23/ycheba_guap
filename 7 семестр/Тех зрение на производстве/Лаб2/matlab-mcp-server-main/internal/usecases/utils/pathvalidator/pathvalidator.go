// Copyright 2025-2026 The MathWorks, Inc.

package pathvalidator

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/matlab/matlab-mcp-server/internal/facades/osfacade"
)

type OSLayer interface {
	Stat(filePath string) (osfacade.FileInfo, error)
}

type PathValidator struct {
	osLayer OSLayer
}

func New(
	osLayer OSLayer,
) *PathValidator {
	return &PathValidator{
		osLayer: osLayer,
	}
}

func (v *PathValidator) ValidateMATLABScript(filePath string) (string, error) {
	absPath, err := resolveAbsolutePath(filePath)
	if err != nil {
		return "", err
	}

	// Check if it's a .m file before doing any file system operations
	if !strings.HasSuffix(absPath, ".m") {
		return "", fmt.Errorf("file must be a MATLAB .m file: %s", absPath)
	}

	fileInfo, err := v.getResourceInfo(absPath)
	if err != nil {
		return "", err
	}

	if fileInfo.IsDir() {
		return "", fmt.Errorf("path is not a file: %s", absPath)
	}

	return absPath, nil
}

func (v *PathValidator) ValidateFolderPath(filePath string) (string, error) {
	absPath, err := resolveAbsolutePath(filePath)
	if err != nil {
		return "", err
	}

	folderInfo, err := v.getResourceInfo(absPath)
	if err != nil {
		return "", err
	}

	if !folderInfo.IsDir() {
		return "", fmt.Errorf("path is not a folder: %s", absPath)
	}

	return absPath, nil
}

func (v *PathValidator) getResourceInfo(filePath string) (osfacade.FileInfo, error) {
	resourceInfo, err := v.osLayer.Stat(filePath)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, fmt.Errorf("resource not found: %s", filePath)
		}
		return nil, fmt.Errorf("error accessing resource: %w", err)
	}

	return resourceInfo, nil
}

func resolveAbsolutePath(filePath string) (string, error) {
	cleanPath := filepath.Clean(filePath)

	if !filepath.IsAbs(cleanPath) {
		return "", fmt.Errorf("%s is not a valid absolute path", cleanPath)
	}

	return cleanPath, nil
}
