// Copyright 2026 The MathWorks, Inc.

package server_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
	internalserver "github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/server"
	publictypesmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/sdk/publictypes"
	"github.com/stretchr/testify/require"
)

func TestNewDefinition_HappyPath(t *testing.T) {
	// Arrange
	mockParameter := &publictypesmocks.MockParameter{}
	defer mockParameter.AssertExpectations(t)

	expectedName := "test-server"
	expectedTitle := "Test Server"
	expectedInstructions := "Test instructions"
	expectedFeatures := publictypes.Features{
		MATLAB: publictypes.MATLABFeature{Enabled: true},
	}
	expectedParameters := []publictypes.Parameter{mockParameter}

	// Act
	definition := internalserver.NewDefinition[struct{}](
		expectedName,
		expectedTitle,
		expectedInstructions,
		expectedFeatures,
		expectedParameters,
		nil,
		nil,
	)

	// Assert
	require.Equal(t, expectedName, definition.Name)
	require.Equal(t, expectedTitle, definition.Title)
	require.Equal(t, expectedInstructions, definition.Instructions)
	require.Equal(t, expectedFeatures, definition.Features)
	require.Equal(t, expectedParameters, definition.Parameters)
	require.Nil(t, definition.DependenciesProvider)
	require.Nil(t, definition.ToolsProvider)
}

func TestNewDefinition_ClonesParametersToPreventMutation(t *testing.T) {
	// Arrange
	mockParameter1 := &publictypesmocks.MockParameter{}
	defer mockParameter1.AssertExpectations(t)

	mockParameter2 := &publictypesmocks.MockParameter{}
	defer mockParameter2.AssertExpectations(t)

	parameters := make([]publictypes.Parameter, 1, 2)
	parameters[0] = mockParameter1

	// Act
	definition := internalserver.NewDefinition[struct{}](
		"test-server",
		"Test Server",
		"Test instructions",
		publictypes.Features{},
		parameters,
		nil,
		nil,
	)

	// Mutate original slice to verify defensive copy
	parameters[0] = mockParameter2

	// Assert
	require.Len(t, definition.Parameters, 1)
	require.Equal(t, mockParameter1, definition.Parameters[0])
}
