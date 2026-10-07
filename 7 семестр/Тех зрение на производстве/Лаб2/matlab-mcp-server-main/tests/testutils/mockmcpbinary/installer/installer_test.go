// Copyright 2026 The MathWorks, Inc.

package installer_test

import (
	"errors"
	"path/filepath"
	"testing"

	mocks "github.com/matlab/matlab-mcp-server/tests/mocks/testutils/mockmcpbinary/installer"
	"github.com/matlab/matlab-mcp-server/tests/testconfig"
	"github.com/matlab/matlab-mcp-server/tests/testutils/mockmcpbinary/installer"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestInstaller_BuildAndInstall_Success(t *testing.T) {
	binDir := filepath.Join("fake", "bin")
	moduleRoot := filepath.Join("fake", "module")

	finder := mocks.NewMockModuleRootFinder(t)
	finder.EXPECT().FindModuleRoot().Return(moduleRoot, nil)

	builder := mocks.NewMockBinaryBuilder(t)
	expectedSourceDir := filepath.Join(moduleRoot, "tests", "testutils", "mockmcpbinary", "source")
	expectedBinaryPath := filepath.Join(binDir, "matlab-mcp-server-"+testconfig.OSName+"-"+testconfig.Architecture+testconfig.ExecutableExtension)
	builder.EXPECT().Build(expectedSourceDir, expectedBinaryPath).Return(nil)

	inst := installer.New(finder, builder)

	binaryPath, err := inst.BuildAndInstall(binDir)

	require.NoError(t, err)
	assert.Equal(t, expectedBinaryPath, binaryPath)
}

func TestInstaller_BuildAndInstall_FindModuleRootFailure(t *testing.T) {
	binDir := filepath.Join("fake", "bin")
	expectedErr := errors.New("module root not found")

	finder := mocks.NewMockModuleRootFinder(t)
	finder.EXPECT().FindModuleRoot().Return("", expectedErr)

	builder := mocks.NewMockBinaryBuilder(t)

	inst := installer.New(finder, builder)

	_, err := inst.BuildAndInstall(binDir)

	require.Error(t, err)
	assert.Contains(t, err.Error(), "finding module root")
	assert.ErrorIs(t, err, expectedErr)
}

func TestInstaller_BuildAndInstall_BuildFailure(t *testing.T) {
	binDir := filepath.Join("fake", "bin")
	moduleRoot := filepath.Join("fake", "module")
	expectedErr := errors.New("build failed")

	finder := mocks.NewMockModuleRootFinder(t)
	finder.EXPECT().FindModuleRoot().Return(moduleRoot, nil)

	builder := mocks.NewMockBinaryBuilder(t)
	builder.EXPECT().Build(
		filepath.Join(moduleRoot, "tests", "testutils", "mockmcpbinary", "source"),
		filepath.Join(binDir, "matlab-mcp-server-"+testconfig.OSName+"-"+testconfig.Architecture+testconfig.ExecutableExtension),
	).Return(expectedErr)

	inst := installer.New(finder, builder)

	_, err := inst.BuildAndInstall(binDir)

	require.Error(t, err)
	assert.Contains(t, err.Error(), "building mock MCP binary")
	assert.ErrorIs(t, err, expectedErr)
}
