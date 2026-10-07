// Copyright 2026 The MathWorks, Inc.

package parameters_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/parameters"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
	internalentities "github.com/matlab/matlab-mcp-server/internal/entities"
	publictypesmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/sdk/publictypes"
	"github.com/stretchr/testify/require"
)

func TestNewFactory_HappyPath(t *testing.T) {
	// Act
	factory := parameters.NewFactory()

	// Assert
	require.NotNil(t, factory)
}

func TestFactory_New_HappyPath(t *testing.T) {
	// Arrange
	mockParam1 := &publictypesmocks.MockParameter{}
	defer mockParam1.AssertExpectations(t)

	mockParam2 := &publictypesmocks.MockParameter{}
	defer mockParam2.AssertExpectations(t)

	factory := parameters.NewFactory()

	// Act
	result := factory.New([]publictypes.Parameter{mockParam1, mockParam2})

	// Assert
	expectedResult := []internalentities.Parameter{mockParam1, mockParam2}
	require.Equal(t, expectedResult, result)
}

func TestFactory_New_EmptySlice(t *testing.T) {
	// Arrange
	factory := parameters.NewFactory()

	// Act
	result := factory.New([]publictypes.Parameter{})

	// Assert
	require.Nil(t, result)
}

func TestFactory_New_NilSlice(t *testing.T) {
	// Arrange
	factory := parameters.NewFactory()

	// Act
	result := factory.New(nil)

	// Assert
	require.Nil(t, result)
}
