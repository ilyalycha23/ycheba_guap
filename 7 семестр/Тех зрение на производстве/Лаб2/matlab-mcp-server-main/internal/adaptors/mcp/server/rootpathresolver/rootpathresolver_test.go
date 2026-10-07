// Copyright 2026 The MathWorks, Inc.

package rootpathresolver_test

import (
	"path/filepath"
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/mcp/server/rootpathresolver"
	"github.com/matlab/matlab-mcp-server/internal/entities"
	mocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/mcp/server/rootpathresolver"
	"github.com/stretchr/testify/require"
)

func TestResolve_LinuxAbsolutePath(t *testing.T) {
	// Arrange
	mockOSLayer := mocks.NewMockOSLayer(t)

	expectedIsAbsArg := "/home/user/project"
	expectedPath := filepath.FromSlash("/home/user/project")

	mockOSLayer.EXPECT().GOOS().Return("linux").Once()
	mockOSLayer.EXPECT().IsAbs(expectedIsAbsArg).Return(true).Once()

	resolver := rootpathresolver.New(mockOSLayer)
	root := entities.NewMCPRoot("file:///home/user/project", "project")

	// Act
	result, err := resolver.Resolve(root)

	// Assert
	require.NoError(t, err)
	require.Equal(t, expectedPath, result)
}

func TestResolve_WindowsDriveLetter(t *testing.T) {
	// Arrange
	mockOSLayer := mocks.NewMockOSLayer(t)

	expectedIsAbsArg := "C:/Users/project"
	expectedPath := filepath.FromSlash("C:/Users/project")

	mockOSLayer.EXPECT().GOOS().Return("windows").Once()
	mockOSLayer.EXPECT().IsAbs(expectedIsAbsArg).Return(true).Once()

	resolver := rootpathresolver.New(mockOSLayer)
	root := entities.NewMCPRoot("file:///C:/Users/project", "project")

	// Act
	result, err := resolver.Resolve(root)

	// Assert
	require.NoError(t, err)
	require.Equal(t, expectedPath, result)
}

func TestResolve_UnsupportedScheme(t *testing.T) {
	// Arrange
	mockOSLayer := mocks.NewMockOSLayer(t)

	resolver := rootpathresolver.New(mockOSLayer)
	root := entities.NewMCPRoot("https://example.com/path", "remote")

	// Act
	_, err := resolver.Resolve(root)

	// Assert
	require.ErrorContains(t, err, "unsupported URI scheme")
}

func TestResolve_NonEmptyHostRejected(t *testing.T) {
	// Arrange
	mockOSLayer := mocks.NewMockOSLayer(t)

	resolver := rootpathresolver.New(mockOSLayer)
	// file://server/share is the RFC 8089 form for UNC path \\server\share.
	// url.Parse produces Host="server", Path="/share".
	root := entities.NewMCPRoot("file://server/share", "unc")

	// Act
	_, err := resolver.Resolve(root)

	// Assert
	require.ErrorContains(t, err, "UNC paths are not supported")
}

func TestResolve_UNCWithEmptyHostOnWindows(t *testing.T) {
	// Arrange
	mockOSLayer := mocks.NewMockOSLayer(t)

	mockOSLayer.EXPECT().GOOS().Return("windows").Once()

	resolver := rootpathresolver.New(mockOSLayer)
	root := entities.NewMCPRoot("file:////server/share", "unc")

	// Act
	_, err := resolver.Resolve(root)

	// Assert
	require.ErrorContains(t, err, "UNC paths are not supported")
}

func TestResolve_DoubleSlashAllowedOnLinux(t *testing.T) {
	// Arrange
	mockOSLayer := mocks.NewMockOSLayer(t)

	expectedIsAbsArg := "//server/share"
	expectedPath := filepath.FromSlash("//server/share")

	mockOSLayer.EXPECT().GOOS().Return("linux").Once()
	mockOSLayer.EXPECT().IsAbs(expectedIsAbsArg).Return(true).Once()

	resolver := rootpathresolver.New(mockOSLayer)
	root := entities.NewMCPRoot("file:////server/share", "doubleslash")

	// Act
	result, err := resolver.Resolve(root)

	// Assert
	require.NoError(t, err)
	require.Equal(t, expectedPath, result)
}

func TestResolve_RelativePathErrors(t *testing.T) {
	// Arrange
	mockOSLayer := mocks.NewMockOSLayer(t)

	expectedIsAbsArg := "/relative/path"

	mockOSLayer.EXPECT().GOOS().Return("linux").Once()
	mockOSLayer.EXPECT().IsAbs(expectedIsAbsArg).Return(false).Once()

	resolver := rootpathresolver.New(mockOSLayer)
	root := entities.NewMCPRoot("file:///relative/path", "rel")

	// Act
	_, err := resolver.Resolve(root)

	// Assert
	require.ErrorContains(t, err, "root path is not absolute")
}
