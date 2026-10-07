// Copyright 2026 The MathWorks, Inc.

package definition_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/application/definition"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/mcp/tools"
	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/testutils"
	toolsmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/mcp/tools"
	basetoolmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/mcp/tools/basetool"
	entitiesmocks "github.com/matlab/matlab-mcp-server/mocks/entities"
	"github.com/stretchr/testify/require"
)

func TestDefinition_Name_HappyPath(t *testing.T) {
	// Arrange
	expectedName := "my-definition"
	def := definition.New(expectedName, "", "", definition.Features{}, nil, nil, nil)

	// Act
	result := def.Name()

	// Assert
	require.Equal(t, expectedName, result)
}

func TestDefinition_Title_HappyPath(t *testing.T) {
	// Arrange
	expectedTitle := "My Definition Title"
	def := definition.New("", expectedTitle, "", definition.Features{}, nil, nil, nil)

	// Act
	result := def.Title()

	// Assert
	require.Equal(t, expectedTitle, result)
}

func TestDefinition_Instructions_HappyPath(t *testing.T) {
	// Arrange
	expectedInstructions := "These are the instructions"
	def := definition.New("", "", expectedInstructions, definition.Features{}, nil, nil, nil)

	// Act
	result := def.Instructions()

	// Assert
	require.Equal(t, expectedInstructions, result)
}

func TestDefinition_Features_HappyPath(t *testing.T) {
	// Arrange
	expectedFeatures := definition.Features{
		MATLAB: definition.MATLABFeature{Enabled: true},
	}
	def := definition.New("", "", "", expectedFeatures, nil, nil, nil)

	// Act
	result := def.Features()

	// Assert
	require.Equal(t, expectedFeatures, result)
}

func TestDefinition_Parameters_HappyPath(t *testing.T) {
	// Arrange
	mockParam1 := &entitiesmocks.MockParameter{}
	defer mockParam1.AssertExpectations(t)

	mockParam2 := &entitiesmocks.MockParameter{}
	defer mockParam2.AssertExpectations(t)

	expectedParameters := []entities.Parameter{mockParam1, mockParam2}
	def := definition.New("", "", "", definition.Features{}, expectedParameters, nil, nil)

	// Act
	result := def.Parameters()

	// Assert
	require.Equal(t, expectedParameters, result)
}

func TestDefinition_Parameters_EmptySlice(t *testing.T) {
	// Arrange
	expectedParameters := []entities.Parameter{}
	def := definition.New("", "", "", definition.Features{}, expectedParameters, nil, nil)

	// Act
	result := def.Parameters()

	// Assert
	require.Equal(t, expectedParameters, result)
}

func TestDefinition_Parameters_Nil(t *testing.T) {
	// Arrange
	def := definition.New("", "", "", definition.Features{}, nil, nil, nil)

	// Act
	result := def.Parameters()

	// Assert
	require.Nil(t, result)
}

func TestDefinition_Dependencies_HappyPath(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	expectedDependencies := &struct{}{}
	expectedResources := definition.DependenciesProviderResources{
		Logger: mockLogger,
	}

	dependenciesProvider := func(resources definition.DependenciesProviderResources) (any, error) {
		require.Equal(t, expectedResources, resources)
		return expectedDependencies, nil
	}

	def := definition.New("", "", "", definition.Features{}, nil, dependenciesProvider, nil)

	// Act
	result, err := def.Dependencies(expectedResources)

	// Assert
	require.NoError(t, err)
	require.Equal(t, expectedDependencies, result)
}

func TestDefinition_Dependencies_NilProvider(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	expectedResources := definition.DependenciesProviderResources{
		Logger: mockLogger,
	}
	def := definition.New("", "", "", definition.Features{}, nil, nil, nil)

	// Act
	result, err := def.Dependencies(expectedResources)

	// Assert
	require.NoError(t, err)
	require.Nil(t, result)
}

func TestDefinition_Tools_HappyPath(t *testing.T) {
	// Arrange
	mockTool := &toolsmocks.MockTool{}
	defer mockTool.AssertExpectations(t)

	mockLoggerFactory := &basetoolmocks.MockLoggerFactory{}
	defer mockLoggerFactory.AssertExpectations(t)

	expectedResources := definition.ToolsProviderResources{
		LoggerFactory: mockLoggerFactory,
	}
	expectedTools := []tools.Tool{mockTool}

	toolsProvider := func(resources definition.ToolsProviderResources) []tools.Tool {
		require.Equal(t, expectedResources, resources)
		return expectedTools
	}

	def := definition.New("", "", "", definition.Features{}, nil, nil, toolsProvider)

	// Act
	result := def.Tools(expectedResources)

	// Assert
	require.Equal(t, expectedTools, result)
}

func TestDefinition_Tools_NilProvider(t *testing.T) {
	// Arrange
	expectedResources := definition.ToolsProviderResources{}
	def := definition.New("", "", "", definition.Features{}, nil, nil, nil)

	// Act
	result := def.Tools(expectedResources)

	// Assert
	require.Nil(t, result)
}
