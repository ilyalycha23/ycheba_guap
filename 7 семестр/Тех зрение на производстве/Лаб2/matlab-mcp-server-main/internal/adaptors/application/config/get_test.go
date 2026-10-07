// Copyright 2025-2026 The MathWorks, Inc.

package config_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/application/config"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/application/parameter/defaultparameters"
	"github.com/matlab/matlab-mcp-server/internal/messages"
	configmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/application/config"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestGet_HappyPath(t *testing.T) {
	// Arrange
	mockConfig := &configmocks.MockGenericConfig{}
	defer mockConfig.AssertExpectations(t)

	parameter := defaultparameters.LogLevel()
	expectedValue := "info"

	mockConfig.EXPECT().
		Get(parameter.GetID()).
		Return(expectedValue, nil).
		Once()

	// Act
	result, err := config.Get(mockConfig, parameter)

	// Assert
	require.NoError(t, err)
	assert.Equal(t, expectedValue, result)
}

func TestGet_GetError(t *testing.T) {
	// Arrange
	mockConfig := &configmocks.MockGenericConfig{}
	defer mockConfig.AssertExpectations(t)

	parameter := defaultparameters.LogLevel()

	mockConfig.EXPECT().
		Get(parameter.GetID()).
		Return(nil, messages.AnError).
		Once()

	// Act
	result, err := config.Get(mockConfig, parameter)

	// Assert
	require.ErrorIs(t, err, messages.AnError)
	assert.Empty(t, result)
}

func TestGet_InvalidType(t *testing.T) {
	// Arrange
	mockConfig := &configmocks.MockGenericConfig{}
	defer mockConfig.AssertExpectations(t)

	parameter := defaultparameters.LogLevel()
	wrongTypeValue := 123

	mockConfig.EXPECT().
		Get(parameter.GetID()).
		Return(wrongTypeValue, nil).
		Once()

	expectedError := messages.New_StartupErrors_InvalidParameterType_Error(parameter.GetID(), "string")

	// Act
	result, err := config.Get(mockConfig, parameter)

	// Assert
	require.Equal(t, expectedError, err)
	assert.Empty(t, result)
}

func TestGet_BoolType_HappyPath(t *testing.T) {
	// Arrange
	mockConfig := &configmocks.MockGenericConfig{}
	defer mockConfig.AssertExpectations(t)

	parameter := defaultparameters.HelpMode()
	expectedValue := true

	mockConfig.EXPECT().
		Get(parameter.GetID()).
		Return(expectedValue, nil).
		Once()

	// Act
	result, err := config.Get(mockConfig, parameter)

	// Assert
	require.NoError(t, err)
	assert.True(t, result)
}

func TestGet_BoolType_InvalidType(t *testing.T) {
	// Arrange
	mockConfig := &configmocks.MockGenericConfig{}
	defer mockConfig.AssertExpectations(t)

	parameter := defaultparameters.HelpMode()
	wrongTypeValue := "true"

	mockConfig.EXPECT().
		Get(parameter.GetID()).
		Return(wrongTypeValue, nil).
		Once()

	expectedError := messages.New_StartupErrors_InvalidParameterType_Error(parameter.GetID(), "bool")

	// Act
	result, err := config.Get(mockConfig, parameter)

	// Assert
	require.Equal(t, expectedError, err)
	assert.False(t, result)
}
