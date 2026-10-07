// Copyright 2026 The MathWorks, Inc.

package installer_test

import (
	"os"
	"testing"

	"github.com/matlab/matlab-mcp-server/tests/testutils/mockmcpbinary/installer"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestGoListModuleRootFinder_ReturnsExistingDirectory(t *testing.T) {
	finder := installer.GoListModuleRootFinder{}

	moduleDir, err := finder.FindModuleRoot()

	require.NoError(t, err)
	require.NotEmpty(t, moduleDir)
	info, err := os.Stat(moduleDir)
	require.NoError(t, err)
	assert.True(t, info.IsDir())
}
