// Copyright 2026 The MathWorks, Inc.

package definition_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/application/definition"
	"github.com/matlab/matlab-mcp-server/internal/testutils"
	configmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/application/config"
	definitionmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/application/definition"
	"github.com/stretchr/testify/require"
)

func TestNewDependenciesProviderResources_HappyPath(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockConfig := &configmocks.MockGenericConfig{}
	defer mockConfig.AssertExpectations(t)

	mockMessageCatalog := &definitionmocks.MockMessageCatalog{}
	defer mockMessageCatalog.AssertExpectations(t)

	mockWatchdog := &definitionmocks.MockWatchdog{}
	defer mockWatchdog.AssertExpectations(t)

	// Act
	result := definition.NewDependenciesProviderResources(
		mockLogger,
		mockConfig,
		mockMessageCatalog,
		mockWatchdog,
	)

	// Assert
	require.Equal(t, mockLogger, result.Logger)
	require.Equal(t, mockConfig, result.Config)
	require.Equal(t, mockMessageCatalog, result.MessageCatalog)
	require.Equal(t, mockWatchdog, result.Watchdog)
}
