// Copyright 2026 The MathWorks, Inc.

//go:build !windows

package mcpb_test

import (
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func assertLauncherPermissions(t *testing.T, launcherSh, launcherCmd string) {
	t.Helper()

	shInfo, err := os.Stat(launcherSh)
	require.NoError(t, err)
	assert.Equal(t, os.FileMode(0o755), shInfo.Mode().Perm(), "launch-matlab-mcp.sh should be executable")

	cmdInfo, err := os.Stat(launcherCmd)
	require.NoError(t, err)
	assert.Equal(t, os.FileMode(0o755), cmdInfo.Mode().Perm(), "launch-matlab-mcp.cmd should be executable")
}
