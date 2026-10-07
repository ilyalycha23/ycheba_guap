// Copyright 2026 The MathWorks, Inc.

package features_test

import (
	"testing"

	internaldefinition "github.com/matlab/matlab-mcp-server/internal/adaptors/application/definition"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/features"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
	"github.com/stretchr/testify/require"
)

func TestNewFactory_HappyPath(t *testing.T) {
	// Act
	factory := features.NewFactory()

	// Assert
	require.NotNil(t, factory)
}

func TestFactory_New_HappyPath(t *testing.T) {
	// Arrange
	factory := features.NewFactory()
	input := publictypes.Features{
		MATLAB: publictypes.MATLABFeature{
			Enabled: true,
		},
	}

	// Act
	result := factory.New(input)

	// Assert
	expectedResult := internaldefinition.Features{
		MATLAB: internaldefinition.MATLABFeature{
			Enabled: true,
		},
	}
	require.Equal(t, expectedResult, result)
}

func TestFactory_New_DefaultValues(t *testing.T) {
	// Arrange
	factory := features.NewFactory()

	// Act
	result := factory.New(publictypes.Features{})

	// Assert
	expectedResult := internaldefinition.Features{}
	require.Equal(t, expectedResult, result)
}
