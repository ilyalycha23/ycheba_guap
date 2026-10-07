// Copyright 2026 The MathWorks, Inc.

package buildinfo_test

import (
	"runtime/debug"
	"testing"

	buildinfoadaptor "github.com/matlab/matlab-mcp-server/internal/adaptors/buildinfo"
	buildinfomocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/buildinfo"
	"github.com/stretchr/testify/require"
)

func TestNew_HappyPath(t *testing.T) {
	// Arrange
	mockOSLayer := buildinfomocks.NewMockOSLayer(t)

	// Act
	result := buildinfoadaptor.New(mockOSLayer)

	// Assert
	require.NotNil(t, result)
}

func TestDebug_Version_HappyPath(t *testing.T) {
	// Arrange
	mockOSLayer := buildinfomocks.NewMockOSLayer(t)

	expectedVersion := "v1.2.3"
	buildInfo := &debug.BuildInfo{
		Main: debug.Module{
			Path:    "github.com/matlab/matlab-mcp-server",
			Version: expectedVersion,
		},
	}

	mockOSLayer.EXPECT().
		ReadBuildInfo().
		Return(buildInfo, true).
		Once()

	d := buildinfoadaptor.New(mockOSLayer)

	// Act
	result := d.Version()

	// Assert
	require.Equal(t, expectedVersion, result)
}

func TestDebug_Version_ReadBuildInfoFails(t *testing.T) {
	// Arrange
	mockOSLayer := buildinfomocks.NewMockOSLayer(t)

	mockOSLayer.EXPECT().
		ReadBuildInfo().
		Return(nil, false).
		Once()

	d := buildinfoadaptor.New(mockOSLayer)

	// Act
	result := d.Version()

	// Assert
	require.Equal(t, "(unknown)", result)
}

func TestDebug_Version_EmptyVersion(t *testing.T) {
	// Arrange
	mockOSLayer := buildinfomocks.NewMockOSLayer(t)

	buildInfo := &debug.BuildInfo{
		Main: debug.Module{
			Path:    "github.com/matlab/matlab-mcp-server",
			Version: "",
		},
	}

	mockOSLayer.EXPECT().
		ReadBuildInfo().
		Return(buildInfo, true).
		Once()

	d := buildinfoadaptor.New(mockOSLayer)

	// Act
	result := d.Version()

	// Assert
	require.Equal(t, "(devel)", result)
}

func TestDebug_Version_DevelVersion(t *testing.T) {
	// Arrange
	mockOSLayer := buildinfomocks.NewMockOSLayer(t)

	buildInfo := &debug.BuildInfo{
		Main: debug.Module{
			Path:    "github.com/matlab/matlab-mcp-server",
			Version: "(devel)",
		},
	}

	mockOSLayer.EXPECT().
		ReadBuildInfo().
		Return(buildInfo, true).
		Once()

	d := buildinfoadaptor.New(mockOSLayer)

	// Act
	result := d.Version()

	// Assert
	require.Equal(t, "(devel)", result)
}

func TestDebug_FullVersion_HappyPath(t *testing.T) {
	// Arrange
	mockOSLayer := buildinfomocks.NewMockOSLayer(t)

	expectedPath := "github.com/matlab/matlab-mcp-server"
	expectedVersion := "v1.2.3"
	buildInfo := &debug.BuildInfo{
		Main: debug.Module{
			Path:    expectedPath,
			Version: expectedVersion,
		},
	}

	mockOSLayer.EXPECT().
		ReadBuildInfo().
		Return(buildInfo, true).
		Once()

	d := buildinfoadaptor.New(mockOSLayer)

	// Act
	result := d.FullVersion()

	// Assert
	require.Equal(t, expectedPath+" "+expectedVersion, result)
}

func TestDebug_FullVersion_ReadBuildInfoFails(t *testing.T) {
	// Arrange
	mockOSLayer := buildinfomocks.NewMockOSLayer(t)

	mockOSLayer.EXPECT().
		ReadBuildInfo().
		Return(nil, false).
		Once()

	d := buildinfoadaptor.New(mockOSLayer)

	// Act
	result := d.FullVersion()

	// Assert
	require.Equal(t, "(unknown)", result)
}

func TestDebug_FullVersion_DevelVersion(t *testing.T) {
	// Arrange
	mockOSLayer := buildinfomocks.NewMockOSLayer(t)

	expectedPath := "github.com/matlab/matlab-mcp-server"
	buildInfo := &debug.BuildInfo{
		Main: debug.Module{
			Path:    expectedPath,
			Version: "(devel)",
		},
	}

	mockOSLayer.EXPECT().
		ReadBuildInfo().
		Return(buildInfo, true).
		Once()

	d := buildinfoadaptor.New(mockOSLayer)

	// Act
	result := d.FullVersion()

	// Assert
	require.Equal(t, expectedPath+" (devel)", result)
}

func TestDebug_FullVersion_EmptyVersion(t *testing.T) {
	// Arrange
	mockOSLayer := buildinfomocks.NewMockOSLayer(t)

	expectedPath := "github.com/matlab/matlab-mcp-server"
	buildInfo := &debug.BuildInfo{
		Main: debug.Module{
			Path:    expectedPath,
			Version: "",
		},
	}

	mockOSLayer.EXPECT().
		ReadBuildInfo().
		Return(buildInfo, true).
		Once()

	d := buildinfoadaptor.New(mockOSLayer)

	// Act
	result := d.FullVersion()

	// Assert
	require.Equal(t, expectedPath+" (devel)", result)
}
