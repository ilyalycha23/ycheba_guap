// Copyright 2026 The MathWorks, Inc.

//go:build windows

package os_test

import (
	"testing"

	osadaptor "github.com/matlab/matlab-mcp-server/internal/adaptors/os"
	osmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/os"
	registryfacademocks "github.com/matlab/matlab-mcp-server/mocks/facades/registryfacade"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"golang.org/x/sys/windows/registry"
)

func TestOS_Version_WithBuildNumber(t *testing.T) {
	// Arrange
	mockOSLayer := &osmocks.MockVersionOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockRegistryLayer := &osmocks.MockRegistryLayer{}
	defer mockRegistryLayer.AssertExpectations(t)

	mockKey := &registryfacademocks.MockRegistryKey{}
	defer mockKey.AssertExpectations(t)

	expectedVersion := "Windows 11 Pro (Build 22631)"

	mockRegistryLayer.EXPECT().
		OpenKey(uintptr(registry.LOCAL_MACHINE), `SOFTWARE\Microsoft\Windows NT\CurrentVersion`, uint32(registry.QUERY_VALUE)).
		Return(mockKey, nil).
		Once()

	mockKey.EXPECT().
		GetStringValue("ProductName").
		Return("Windows 11 Pro", uint32(0), nil).
		Once()

	mockKey.EXPECT().
		GetStringValue("CurrentBuildNumber").
		Return("22631", uint32(0), nil).
		Once()

	mockKey.EXPECT().
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

func TestOS_Version_WithoutBuildNumber(t *testing.T) {
	// Arrange
	mockOSLayer := &osmocks.MockVersionOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockRegistryLayer := &osmocks.MockRegistryLayer{}
	defer mockRegistryLayer.AssertExpectations(t)

	mockKey := &registryfacademocks.MockRegistryKey{}
	defer mockKey.AssertExpectations(t)

	expectedVersion := "Windows 11 Pro"

	mockRegistryLayer.EXPECT().
		OpenKey(uintptr(registry.LOCAL_MACHINE), `SOFTWARE\Microsoft\Windows NT\CurrentVersion`, uint32(registry.QUERY_VALUE)).
		Return(mockKey, nil).
		Once()

	mockKey.EXPECT().
		GetStringValue("ProductName").
		Return("Windows 11 Pro", uint32(0), nil).
		Once()

	mockKey.EXPECT().
		GetStringValue("CurrentBuildNumber").
		Return("", uint32(0), assert.AnError).
		Once()

	mockKey.EXPECT().
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

func TestOS_Version_OpenKeyError(t *testing.T) {
	// Arrange
	mockOSLayer := &osmocks.MockVersionOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockRegistryLayer := &osmocks.MockRegistryLayer{}
	defer mockRegistryLayer.AssertExpectations(t)

	mockRegistryLayer.EXPECT().
		OpenKey(uintptr(registry.LOCAL_MACHINE), `SOFTWARE\Microsoft\Windows NT\CurrentVersion`, uint32(registry.QUERY_VALUE)).
		Return(nil, assert.AnError).
		Once()

	osInstance := osadaptor.New(mockOSLayer, mockRegistryLayer)

	// Act
	version, err := osInstance.Version()

	// Assert
	require.ErrorIs(t, err, assert.AnError)
	assert.Empty(t, version)
}

func TestOS_Version_ProductNameError(t *testing.T) {
	// Arrange
	mockOSLayer := &osmocks.MockVersionOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockRegistryLayer := &osmocks.MockRegistryLayer{}
	defer mockRegistryLayer.AssertExpectations(t)

	mockKey := &registryfacademocks.MockRegistryKey{}
	defer mockKey.AssertExpectations(t)

	mockRegistryLayer.EXPECT().
		OpenKey(uintptr(registry.LOCAL_MACHINE), `SOFTWARE\Microsoft\Windows NT\CurrentVersion`, uint32(registry.QUERY_VALUE)).
		Return(mockKey, nil).
		Once()

	mockKey.EXPECT().
		GetStringValue("ProductName").
		Return("", uint32(0), assert.AnError).
		Once()

	mockKey.EXPECT().
		Close().
		Return(nil).
		Once()

	osInstance := osadaptor.New(mockOSLayer, mockRegistryLayer)

	// Act
	version, err := osInstance.Version()

	// Assert
	require.ErrorIs(t, err, assert.AnError)
	assert.Empty(t, version)
}
