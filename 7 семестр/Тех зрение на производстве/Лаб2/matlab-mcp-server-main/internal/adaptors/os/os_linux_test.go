// Copyright 2026 The MathWorks, Inc.

//go:build linux

package os_test

import (
	"io"
	"path/filepath"
	"strings"
	"testing"

	osadaptor "github.com/matlab/matlab-mcp-server/internal/adaptors/os"
	osmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/os"
	osfacademocks "github.com/matlab/matlab-mcp-server/mocks/facades/osfacade"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
	"github.com/stretchr/testify/require"
)

func TestOS_Version_NameAndVersion(t *testing.T) {
	// Arrange
	mockOSLayer := &osmocks.MockVersionOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockRegistryLayer := &osmocks.MockRegistryLayer{}
	defer mockRegistryLayer.AssertExpectations(t)

	mockFile := &osfacademocks.MockFile{}
	defer mockFile.AssertExpectations(t)

	osReleaseContent := "NAME=\"Debian GNU/Linux\"\nVERSION_ID=\"12\"\n"
	reader := strings.NewReader(osReleaseContent)
	expectedPath := filepath.Join("/etc", "os-release")
	expectedVersion := "Debian GNU/Linux 12"

	mockOSLayer.EXPECT().
		Open(expectedPath).
		Return(mockFile, nil).
		Once()

	mockFile.EXPECT().
		Read(mock.Anything).
		RunAndReturn(func(b []byte) (int, error) {
			return reader.Read(b)
		})

	mockFile.EXPECT().
		Close().
		Return(nil).
		Once()

	osInstance := osadaptor.New(mockOSLayer, mockRegistryLayer)

	// Act
	version, err := osInstance.Version()

	// Assert
	require.NoError(t, err)
	assert.Equal(t, expectedVersion, version)
}

func TestOS_Version_NameOnly(t *testing.T) {
	// Arrange
	mockOSLayer := &osmocks.MockVersionOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockRegistryLayer := &osmocks.MockRegistryLayer{}
	defer mockRegistryLayer.AssertExpectations(t)

	mockFile := &osfacademocks.MockFile{}
	defer mockFile.AssertExpectations(t)

	osReleaseContent := "NAME=\"Arch Linux\"\n"
	reader := strings.NewReader(osReleaseContent)
	expectedPath := filepath.Join("/etc", "os-release")
	expectedVersion := "Arch Linux"

	mockOSLayer.EXPECT().
		Open(expectedPath).
		Return(mockFile, nil).
		Once()

	mockFile.EXPECT().
		Read(mock.Anything).
		RunAndReturn(func(b []byte) (int, error) {
			return reader.Read(b)
		})

	mockFile.EXPECT().
		Close().
		Return(nil).
		Once()

	osInstance := osadaptor.New(mockOSLayer, mockRegistryLayer)

	// Act
	version, err := osInstance.Version()

	// Assert
	require.NoError(t, err)
	assert.Equal(t, expectedVersion, version)
}

func TestOS_Version_EmptyFile(t *testing.T) {
	// Arrange
	mockOSLayer := &osmocks.MockVersionOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockRegistryLayer := &osmocks.MockRegistryLayer{}
	defer mockRegistryLayer.AssertExpectations(t)

	mockFile := &osfacademocks.MockFile{}
	defer mockFile.AssertExpectations(t)

	reader := strings.NewReader("")
	expectedPath := filepath.Join("/etc", "os-release")

	mockOSLayer.EXPECT().
		Open(expectedPath).
		Return(mockFile, nil).
		Once()

	mockFile.EXPECT().
		Read(mock.Anything).
		RunAndReturn(func(b []byte) (int, error) {
			return reader.Read(b)
		})

	mockFile.EXPECT().
		Close().
		Return(nil).
		Once()

	osInstance := osadaptor.New(mockOSLayer, mockRegistryLayer)

	// Act
	version, err := osInstance.Version()

	// Assert
	require.NoError(t, err)
	assert.Equal(t, "Linux", version)
}

func TestOS_Version_OpenError(t *testing.T) {
	// Arrange
	mockOSLayer := &osmocks.MockVersionOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockRegistryLayer := &osmocks.MockRegistryLayer{}
	defer mockRegistryLayer.AssertExpectations(t)

	expectedPath := filepath.Join("/etc", "os-release")

	mockOSLayer.EXPECT().
		Open(expectedPath).
		Return(nil, assert.AnError).
		Once()

	osInstance := osadaptor.New(mockOSLayer, mockRegistryLayer)

	// Act
	version, err := osInstance.Version()

	// Assert
	require.ErrorIs(t, err, assert.AnError)
	assert.Empty(t, version)
}

func TestOS_Version_ScannerError(t *testing.T) {
	// Arrange
	mockOSLayer := &osmocks.MockVersionOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockRegistryLayer := &osmocks.MockRegistryLayer{}
	defer mockRegistryLayer.AssertExpectations(t)

	mockFile := &osfacademocks.MockFile{}
	defer mockFile.AssertExpectations(t)

	expectedPath := filepath.Join("/etc", "os-release")

	mockOSLayer.EXPECT().
		Open(expectedPath).
		Return(mockFile, nil).
		Once()

	callCount := 0
	mockFile.EXPECT().
		Read(mock.Anything).
		RunAndReturn(func(b []byte) (int, error) {
			if callCount == 0 {
				callCount++
				n := copy(b, "NAME=\"Ubuntu\"\n")
				return n, nil
			}
			return 0, io.ErrUnexpectedEOF
		})

	mockFile.EXPECT().
		Close().
		Return(nil).
		Once()

	osInstance := osadaptor.New(mockOSLayer, mockRegistryLayer)

	// Act
	version, err := osInstance.Version()

	// Assert
	require.ErrorIs(t, err, io.ErrUnexpectedEOF)
	assert.Empty(t, version)
}
