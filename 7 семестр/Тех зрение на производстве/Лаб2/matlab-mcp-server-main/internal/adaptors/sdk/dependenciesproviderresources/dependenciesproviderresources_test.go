// Copyright 2026 The MathWorks, Inc.

package dependenciesproviderresources_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/application/definition"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/dependenciesproviderresources"
	internalconfigmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/application/config"
	definitionmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/application/definition"
	dependenciesproviderresourcesmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/sdk/dependenciesproviderresources"
	publictypesmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/sdk/publictypes"
	entitiesmocks "github.com/matlab/matlab-mcp-server/mocks/entities"
	"github.com/stretchr/testify/require"
)

func TestNewFactory_HappyPath(t *testing.T) {
	// Arrange
	mockLoggerFactory := &dependenciesproviderresourcesmocks.MockLoggerFactory{}
	defer mockLoggerFactory.AssertExpectations(t)

	mockConfigFactory := &dependenciesproviderresourcesmocks.MockConfigFactory{}
	defer mockConfigFactory.AssertExpectations(t)

	mockWatchdogFactory := &dependenciesproviderresourcesmocks.MockWatchdogFactory{}
	defer mockWatchdogFactory.AssertExpectations(t)

	// Act
	factory := dependenciesproviderresources.NewFactory(
		mockLoggerFactory,
		mockConfigFactory,
		mockWatchdogFactory,
	)

	// Assert
	require.NotNil(t, factory)
}

func TestFactory_New_HappyPath(t *testing.T) {
	// Arrange
	mockLoggerFactory := &dependenciesproviderresourcesmocks.MockLoggerFactory{}
	defer mockLoggerFactory.AssertExpectations(t)

	mockConfigFactory := &dependenciesproviderresourcesmocks.MockConfigFactory{}
	defer mockConfigFactory.AssertExpectations(t)

	mockWatchdogFactory := &dependenciesproviderresourcesmocks.MockWatchdogFactory{}
	defer mockWatchdogFactory.AssertExpectations(t)

	mockInternalLogger := &entitiesmocks.MockLogger{}
	defer mockInternalLogger.AssertExpectations(t)

	mockInternalConfig := &internalconfigmocks.MockGenericConfig{}
	defer mockInternalConfig.AssertExpectations(t)

	mockMessageCatalog := &definitionmocks.MockMessageCatalog{}
	defer mockMessageCatalog.AssertExpectations(t)

	mockWatchdog := &definitionmocks.MockWatchdog{}
	defer mockWatchdog.AssertExpectations(t)

	mockLoggerFactory.EXPECT().
		New(mockInternalLogger).
		Return(nil).
		Once()

	mockConfigFactory.EXPECT().
		New(mockInternalConfig, mockMessageCatalog).
		Return(nil).
		Once()

	mockWatchdogFactory.EXPECT().
		New(mockInternalLogger, mockWatchdog).
		Return(nil).
		Once()

	internalResources := definition.NewDependenciesProviderResources(
		mockInternalLogger,
		mockInternalConfig,
		mockMessageCatalog,
		mockWatchdog,
	)

	// Act
	resources := dependenciesproviderresources.NewFactory(
		mockLoggerFactory,
		mockConfigFactory,
		mockWatchdogFactory,
	).New(internalResources)

	// Assert
	require.NotNil(t, resources)
}

func TestFactory_New_Logger(t *testing.T) {
	// Arrange
	mockLoggerFactory := &dependenciesproviderresourcesmocks.MockLoggerFactory{}
	defer mockLoggerFactory.AssertExpectations(t)

	mockConfigFactory := &dependenciesproviderresourcesmocks.MockConfigFactory{}
	defer mockConfigFactory.AssertExpectations(t)

	mockWatchdogFactory := &dependenciesproviderresourcesmocks.MockWatchdogFactory{}
	defer mockWatchdogFactory.AssertExpectations(t)

	mockInternalLogger := &entitiesmocks.MockLogger{}
	defer mockInternalLogger.AssertExpectations(t)

	mockInternalConfig := &internalconfigmocks.MockGenericConfig{}
	defer mockInternalConfig.AssertExpectations(t)

	mockMessageCatalog := &definitionmocks.MockMessageCatalog{}
	defer mockMessageCatalog.AssertExpectations(t)

	mockWatchdog := &definitionmocks.MockWatchdog{}
	defer mockWatchdog.AssertExpectations(t)

	expectedLogger := &publictypesmocks.MockLogger{}
	defer expectedLogger.AssertExpectations(t)

	mockLoggerFactory.EXPECT().
		New(mockInternalLogger).
		Return(expectedLogger).
		Once()

	mockConfigFactory.EXPECT().
		New(mockInternalConfig, mockMessageCatalog).
		Return(nil).
		Once()

	mockWatchdogFactory.EXPECT().
		New(mockInternalLogger, mockWatchdog).
		Return(nil).
		Once()

	internalResources := definition.NewDependenciesProviderResources(
		mockInternalLogger,
		mockInternalConfig,
		mockMessageCatalog,
		mockWatchdog,
	)

	// Act
	resources := dependenciesproviderresources.NewFactory(
		mockLoggerFactory,
		mockConfigFactory,
		mockWatchdogFactory,
	).New(internalResources)

	// Assert
	require.Equal(t, expectedLogger, resources.Logger())
}

func TestFactory_New_Config(t *testing.T) {
	// Arrange
	mockLoggerFactory := &dependenciesproviderresourcesmocks.MockLoggerFactory{}
	defer mockLoggerFactory.AssertExpectations(t)

	mockConfigFactory := &dependenciesproviderresourcesmocks.MockConfigFactory{}
	defer mockConfigFactory.AssertExpectations(t)

	mockWatchdogFactory := &dependenciesproviderresourcesmocks.MockWatchdogFactory{}
	defer mockWatchdogFactory.AssertExpectations(t)

	mockInternalLogger := &entitiesmocks.MockLogger{}
	defer mockInternalLogger.AssertExpectations(t)

	mockInternalConfig := &internalconfigmocks.MockGenericConfig{}
	defer mockInternalConfig.AssertExpectations(t)

	mockMessageCatalog := &definitionmocks.MockMessageCatalog{}
	defer mockMessageCatalog.AssertExpectations(t)

	mockWatchdog := &definitionmocks.MockWatchdog{}
	defer mockWatchdog.AssertExpectations(t)

	expectedConfig := &publictypesmocks.MockConfig{}
	defer expectedConfig.AssertExpectations(t)

	mockLoggerFactory.EXPECT().
		New(mockInternalLogger).
		Return(nil).
		Once()

	mockConfigFactory.EXPECT().
		New(mockInternalConfig, mockMessageCatalog).
		Return(expectedConfig).
		Once()

	mockWatchdogFactory.EXPECT().
		New(mockInternalLogger, mockWatchdog).
		Return(nil).
		Once()

	internalResources := definition.NewDependenciesProviderResources(
		mockInternalLogger,
		mockInternalConfig,
		mockMessageCatalog,
		mockWatchdog,
	)

	// Act
	resources := dependenciesproviderresources.NewFactory(
		mockLoggerFactory,
		mockConfigFactory,
		mockWatchdogFactory,
	).New(internalResources)

	// Assert
	require.Equal(t, expectedConfig, resources.Config())
}

func TestFactory_New_Watchdog(t *testing.T) {
	// Arrange
	mockLoggerFactory := &dependenciesproviderresourcesmocks.MockLoggerFactory{}
	defer mockLoggerFactory.AssertExpectations(t)

	mockConfigFactory := &dependenciesproviderresourcesmocks.MockConfigFactory{}
	defer mockConfigFactory.AssertExpectations(t)

	mockWatchdogFactory := &dependenciesproviderresourcesmocks.MockWatchdogFactory{}
	defer mockWatchdogFactory.AssertExpectations(t)

	mockInternalLogger := &entitiesmocks.MockLogger{}
	defer mockInternalLogger.AssertExpectations(t)

	mockInternalConfig := &internalconfigmocks.MockGenericConfig{}
	defer mockInternalConfig.AssertExpectations(t)

	mockMessageCatalog := &definitionmocks.MockMessageCatalog{}
	defer mockMessageCatalog.AssertExpectations(t)

	mockWatchdog := &definitionmocks.MockWatchdog{}
	defer mockWatchdog.AssertExpectations(t)

	expectedWatchdog := &publictypesmocks.MockWatchdog{}
	defer expectedWatchdog.AssertExpectations(t)

	mockLoggerFactory.EXPECT().
		New(mockInternalLogger).
		Return(nil).
		Once()

	mockConfigFactory.EXPECT().
		New(mockInternalConfig, mockMessageCatalog).
		Return(nil).
		Once()

	mockWatchdogFactory.EXPECT().
		New(mockInternalLogger, mockWatchdog).
		Return(expectedWatchdog).
		Once()

	internalResources := definition.NewDependenciesProviderResources(
		mockInternalLogger,
		mockInternalConfig,
		mockMessageCatalog,
		mockWatchdog,
	)

	// Act
	resources := dependenciesproviderresources.NewFactory(
		mockLoggerFactory,
		mockConfigFactory,
		mockWatchdogFactory,
	).New(internalResources)

	// Assert
	require.Equal(t, expectedWatchdog, resources.Watchdog())
}
