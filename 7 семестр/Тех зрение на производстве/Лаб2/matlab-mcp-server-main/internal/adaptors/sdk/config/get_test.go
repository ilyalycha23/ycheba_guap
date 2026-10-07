// Copyright 2026 The MathWorks, Inc.

package config_test

import (
	"testing"

	configadaptor "github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/config"
	publictypesmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/sdk/publictypes"
	"github.com/stretchr/testify/require"
)

func TestGet_HappyPath_String(t *testing.T) {
	// Arrange
	mockConfig := &publictypesmocks.MockConfig{}
	defer mockConfig.AssertExpectations(t)

	expectedKey := "test-key"
	expectedValue := "test-value"

	mockConfig.EXPECT().
		Get(expectedKey, "").
		Return(expectedValue, nil).
		Once()

	param := testParameter[string]{id: expectedKey}

	// Act
	result, err := configadaptor.Get[string](mockConfig, param)

	// Assert
	require.NoError(t, err)
	require.Equal(t, expectedValue, result)
}

func TestGet_HappyPath_Bool(t *testing.T) {
	// Arrange
	mockConfig := &publictypesmocks.MockConfig{}
	defer mockConfig.AssertExpectations(t)

	expectedKey := "bool-key"
	expectedValue := true

	mockConfig.EXPECT().
		Get(expectedKey, false).
		Return(expectedValue, nil).
		Once()

	param := testParameter[bool]{id: expectedKey}

	// Act
	result, err := configadaptor.Get[bool](mockConfig, param)

	// Assert
	require.NoError(t, err)
	require.Equal(t, expectedValue, result)
}

func TestGet_ConfigError(t *testing.T) {
	// Arrange
	mockConfig := &publictypesmocks.MockConfig{}
	defer mockConfig.AssertExpectations(t)

	expectedKey := "missing-key"
	expectedError := anI18nError

	mockConfig.EXPECT().
		Get(expectedKey, "").
		Return(nil, expectedError).
		Once()

	param := testParameter[string]{id: expectedKey}

	// Act
	result, err := configadaptor.Get[string](mockConfig, param)

	// Assert
	require.ErrorIs(t, err, expectedError)
	require.Empty(t, result)
}

func TestGet_CastFailure(t *testing.T) {
	// Arrange
	mockConfig := &publictypesmocks.MockConfig{}
	defer mockConfig.AssertExpectations(t)

	expectedKey := "test-key"

	mockConfig.EXPECT().
		Get(expectedKey, "").
		Return(123, nil).
		Once()

	param := testParameter[string]{id: expectedKey}

	// Act
	result, err := configadaptor.Get[string](mockConfig, param)

	// Assert
	require.NoError(t, err)
	require.Empty(t, result)
}

type testParameter[T interface{ string | bool }] struct {
	id string
}

func (p testParameter[T]) GetID() string {
	return p.id
}
