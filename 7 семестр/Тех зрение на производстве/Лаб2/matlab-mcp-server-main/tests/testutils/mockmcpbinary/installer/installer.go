// Copyright 2026 The MathWorks, Inc.

package installer

import (
	"fmt"
	"path/filepath"

	"github.com/matlab/matlab-mcp-server/tests/testconfig"
)

type ModuleRootFinder interface {
	FindModuleRoot() (string, error)
}

type BinaryBuilder interface {
	Build(sourceDir, outputPath string) error
}

type Installer struct {
	moduleRootFinder ModuleRootFinder
	binaryBuilder    BinaryBuilder
}

func New(moduleRootFinder ModuleRootFinder, binaryBuilder BinaryBuilder) *Installer {
	return &Installer{
		moduleRootFinder: moduleRootFinder,
		binaryBuilder:    binaryBuilder,
	}
}

func (i *Installer) BuildAndInstall(binDir string) (string, error) {
	binaryPath := filepath.Join(binDir, fmt.Sprintf("matlab-mcp-server-%s-%s%s", testconfig.OSName, testconfig.Architecture, testconfig.ExecutableExtension))

	moduleRoot, err := i.moduleRootFinder.FindModuleRoot()
	if err != nil {
		return "", fmt.Errorf("finding module root: %w", err)
	}

	sourceDir := filepath.Join(moduleRoot, "tests", "testutils", "mockmcpbinary", "source")
	if err := i.binaryBuilder.Build(sourceDir, binaryPath); err != nil {
		return "", fmt.Errorf("building mock MCP binary: %w", err)
	}

	return binaryPath, nil
}
