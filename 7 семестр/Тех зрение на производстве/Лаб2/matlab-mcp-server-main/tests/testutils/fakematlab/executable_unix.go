// Copyright 2026 The MathWorks, Inc.
//go:build !windows

package fakematlab

import (
	"os"
	"os/exec"
	"path/filepath"
	"testing"

	"github.com/matlab/matlab-mcp-server/tests/testconfig"
	"github.com/stretchr/testify/require"
)

// buildAndInstall compiles the fake MATLAB binary and places it in the
// directory layout expected by the MCP server on Unix platforms.
func buildAndInstall(t *testing.T, sourceDir, _, binDir string) {
	t.Helper()

	err := os.MkdirAll(binDir, 0o700)
	require.NoError(t, err)

	binExePath := filepath.Join(binDir, testconfig.MATLABExeName)
	buildCmd := exec.Command("go", "build", "-o", binExePath, ".") //nolint:gosec // Trusted test path
	buildCmd.Dir = sourceDir
	buildOutput, err := buildCmd.CombinedOutput()
	require.NoError(t, err, "go build failed: %s", string(buildOutput))
}
