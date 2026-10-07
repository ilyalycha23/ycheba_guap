// Copyright 2026 The MathWorks, Inc.
//go:build windows

package fakematlab

import (
	"os"
	"os/exec"
	"path/filepath"
	"testing"

	matlabservicesconfig "github.com/matlab/matlab-mcp-server/internal/adaptors/matlabmanager/matlabservices/config"
	"github.com/matlab/matlab-mcp-server/tests/testconfig"
	"github.com/stretchr/testify/require"
)

// buildAndInstall compiles the fake MATLAB binary and places it in the
// Windows-specific directory layout expected by the MCP server.
func buildAndInstall(t *testing.T, sourceDir, root, binDir string) {
	t.Helper()

	archDir := filepath.Join(binDir, matlabservicesconfig.ArchFolder)
	err := os.MkdirAll(archDir, 0o700)
	require.NoError(t, err)

	// Compile the fake MATLAB binary into the arch-specific location.
	archExePath := filepath.Join(archDir, matlabservicesconfig.ArchSpecificExeName)
	buildCmd := exec.Command("go", "build", "-o", archExePath, ".") //nolint:gosec // Trusted test path
	buildCmd.Dir = sourceDir
	buildOutput, err := buildCmd.CombinedOutput()
	require.NoError(t, err, "go build failed: %s", string(buildOutput))

	// Copy the compiled binary to the bin directory for PATH discovery.
	binExePath := filepath.Join(binDir, testconfig.MATLABExeName)
	data, err := os.ReadFile(archExePath) //nolint:gosec // Trusted test path
	require.NoError(t, err)
	err = os.WriteFile(binExePath, data, 0o700) //nolint:gosec // Fake executable for tests
	require.NoError(t, err)
}
