// Copyright 2026 The MathWorks, Inc.

package toolcallrequest_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/toolcallrequest"
	configmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/application/config"
	definitionmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/application/definition"
	publictypesmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/sdk/publictypes"
	toolcallrequestmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/sdk/toolcallrequest"
	entitiesmocks "github.com/matlab/matlab-mcp-server/mocks/entities"
	"github.com/stretchr/testify/require"
)

func TestNewFactory_HappyPath(t *testing.T) {
	// Arrange
	mockLoggerFactory := &toolcallrequestmocks.MockLoggerFactory{}
	defer mockLoggerFactory.AssertExpectations(t)

	mockConfigFactory := &toolcallrequestmocks.MockConfigFactory{}
	defer mockConfigFactory.AssertExpectations(t)

	// Act
	factory := toolcallrequest.NewFactory(mockLoggerFactory, mockConfigFactory)

	// Assert
	require.NotNil(t, factory)
}

func TestFactory_New_HappyPath(t *testing.T) {
	// Arrange
	mockLoggerFactory := &toolcallrequestmocks.MockLoggerFactory{}
	defer mockLoggerFactory.AssertExpectations(t)

	mockConfigFactory := &toolcallrequestmocks.MockConfigFactory{}
	defer mockConfigFactory.AssertExpectations(t)

	mockInternalLogger := &entitiesmocks.MockLogger{}
	defer mockInternalLogger.AssertExpectations(t)

	mockInternalConfig := &configmocks.MockGenericConfig{}
	defer mockInternalConfig.AssertExpectations(t)

	mockMessageCatalog := &definitionmocks.MockMessageCatalog{}
	defer mockMessageCatalog.AssertExpectations(t)

	mockLoggerFactory.EXPECT().
		New(mockInternalLogger).
		Return(nil).
		Once()

	mockConfigFactory.EXPECT().
		New(mockInternalConfig, mockMessageCatalog).
		Return(nil).
		Once()

	// Act
	request := toolcallrequest.NewFactory(mockLoggerFactory, mockConfigFactory).New(
		mockInternalLogger,
		mockInternalConfig,
		mockMessageCatalog,
	)

	// Assert
	require.NotNil(t, request)
}

func TestFactory_New_Logger(t *testing.T) {
	// Arrange
	mockLoggerFactory := &toolcallrequestmocks.MockLoggerFactory{}
	defer mockLoggerFactory.AssertExpectations(t)

	mockConfigFactory := &toolcallrequestmocks.MockConfigFactory{}
	defer mockConfigFactory.AssertExpectations(t)

	mockInternalLogger := &entitiesmocks.MockLogger{}
	defer mockInternalLogger.AssertExpectations(t)

	mockInternalConfig := &configmocks.MockGenericConfig{}
	defer mockInternalConfig.AssertExpectations(t)

	mockMessageCatalog := &definitionmocks.MockMessageCatalog{}
	defer mockMessageCatalog.AssertExpectations(t)

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

	request := toolcallrequest.NewFactory(mockLoggerFactory, mockConfigFactory).New(
		mockInternalLogger,
		mockInternalConfig,
		mockMessageCatalog,
	)

	// Act
	result := request.Logger()

	// Assert
	require.Equal(t, expectedLogger, result)
}

func TestFactory_New_Config(t *testing.T) {
	// Arrange
	mockLoggerFactory := &toolcallrequestmocks.MockLoggerFactory{}
	defer mockLoggerFactory.AssertExpectations(t)

	mockConfigFactory := &toolcallrequestmocks.MockConfigFactory{}
	defer mockConfigFactory.AssertExpectations(t)

	mockInternalLogger := &entitiesmocks.MockLogger{}
	defer mockInternalLogger.AssertExpectations(t)

	mockInternalConfig := &configmocks.MockGenericConfig{}
	defer mockInternalConfig.AssertExpectations(t)

	mockMessageCatalog := &definitionmocks.MockMessageCatalog{}
	defer mockMessageCatalog.AssertExpectations(t)

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

	request := toolcallrequest.NewFactory(mockLoggerFactory, mockConfigFactory).New(
		mockInternalLogger,
		mockInternalConfig,
		mockMessageCatalog,
	)

	// Act
	result := request.Config()

	// Assert
	require.Equal(t, expectedConfig, result)
}
