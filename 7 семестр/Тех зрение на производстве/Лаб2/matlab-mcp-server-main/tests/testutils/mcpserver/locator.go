// Copyright 2025-2026 The MathWorks, Inc.

package mcpserver

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/matlab/matlab-mcp-server/tests/testconfig"
	"github.com/matlab/matlab-mcp-server/tests/testutils/facades/filefacade"
	"github.com/matlab/matlab-mcp-server/tests/testutils/facades/osfacade"
)

const matlabMCPServerServerBuildDirEnvironmentVariable = "MATLAB_MCP_SERVER_BUILD_DIR"

// Environment defines the interface for environment variable operations
type Environment interface {
	Getenv(key string) string
}

// FileSystem defines the interface for file system operations
type FileSystem interface {
	Stat(name string) (os.FileInfo, error)
}

type Locator struct {
	Env Environment
	FS  FileSystem
}

func NewLocator() *Locator {
	return &Locator{
		Env: osfacade.RealEnvironment{},
		FS:  filefacade.RealFileSystem{},
	}
}

func (l *Locator) GetPath() (string, error) {
	var path string
	var value string
	if value = l.Env.Getenv(matlabMCPServerServerBuildDirEnvironmentVariable); value == "" {
		return "", fmt.Errorf("environment variable %s is not set", matlabMCPServerServerBuildDirEnvironmentVariable)
	}

	path = filepath.Join(value, testconfig.OSDescriptor, testconfig.MATLABMCPServerBinariesFilename)

	if !filepath.IsAbs(path) {
		return "", fmt.Errorf("mcp server path must be absolute: %s", path)
	}

	if path == "" {
		return "", fmt.Errorf("MATLAB MCP Server binary path cannot be empty")
	}

	if _, err := l.FS.Stat(path); err != nil {
		return "", fmt.Errorf("MATLAB MCP Server binary does not exist at path: %s", path)
	}

	return path, nil
}
