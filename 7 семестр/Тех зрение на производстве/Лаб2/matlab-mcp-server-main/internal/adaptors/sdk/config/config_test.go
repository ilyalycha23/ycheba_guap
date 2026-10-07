// Copyright 2026 The MathWorks, Inc.

package config_test

import (
	"testing"

	configadaptor "github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/config"
	"github.com/matlab/matlab-mcp-server/internal/messages"
	configmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/sdk/config"
	messagesmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/sdk/messages"
	"github.com/stretchr/testify/require"
)

func TestNewFactory_HappyPath(t *testing.T) {
	// Arrange
	mockMessagesFactory := &configmocks.MockMessagesFactory{}
	defer mockMessagesFactory.AssertExpectations(t)

	// Act
	factory := configadaptor.NewFactory(mockMessagesFactory)

	// Assert
	require.NotNil(t, factory)
}

func TestFactory_New_HappyPath(t *testing.T) {
	// Arrange
	mockConfig := &configmocks.MockInternalConfig{}
	defer mockConfig.AssertExpectations(t)

	mockMessageCatalog := &configmocks.MockInternalMessageCatalog{}
	defer mockMessageCatalog.AssertExpectations(t)

	mockMessagesFactory := &configmocks.MockMessagesFactory{}
	defer mockMessagesFactory.AssertExpectations(t)

	mockErrorFactory := &messagesmocks.MockI18nErrorFactory{}
	defer mockErrorFactory.AssertExpectations(t)

	mockMessagesFactory.EXPECT().
		New(mockMessageCatalog).
		Return(mockErrorFactory).
		Once()

	// Act
	adaptor := configadaptor.NewFactory(mockMessagesFactory).New(mockConfig, mockMessageCatalog)

	// Assert
	require.NotNil(t, adaptor)
}

func TestConfig_Get_HappyPath(t *testing.T) {
	// Arrange
	mockConfig := &configmocks.MockInternalConfig{}
	defer mockConfig.AssertExpectations(t)

	mockMessageCatalog := &configmocks.MockInternalMessageCatalog{}
	defer mockMessageCatalog.AssertExpectations(t)

	mockMessagesFactory := &configmocks.MockMessagesFactory{}
	defer mockMessagesFactory.AssertExpectations(t)

	mockErrorFactory := &messagesmocks.MockI18nErrorFactory{}
	defer mockErrorFactory.AssertExpectations(t)

	expectedKey := "test-key"
	expectedValue := "test-value"

	mockMessagesFactory.EXPECT().
		New(mockMessageCatalog).
		Return(mockErrorFactory).
		Once()

	mockConfig.EXPECT().
		Get(expectedKey).
		Return(expectedValue, nil).
		Once()

	adaptor := configadaptor.NewFactory(mockMessagesFactory).New(mockConfig, mockMessageCatalog)

	// Act
	result, err := adaptor.Get(expectedKey, "")

	// Assert
	require.NoError(t, err)
	require.Equal(t, expectedValue, result)
}

func TestConfig_Get_ConfigError(t *testing.T) {
	// Arrange
	mockConfig := &configmocks.MockInternalConfig{}
	defer mockConfig.AssertExpectations(t)

	mockMessageCatalog := &configmocks.MockInternalMessageCatalog{}
	defer mockMessageCatalog.AssertExpectations(t)

	mockMessagesFactory := &configmocks.MockMessagesFactory{}
	defer mockMessagesFactory.AssertExpectations(t)

	mockErrorFactory := &messagesmocks.MockI18nErrorFactory{}
	defer mockErrorFactory.AssertExpectations(t)

	expectedKey := "missing-key"
	expectedError := anI18nError

	mockMessagesFactory.EXPECT().
		New(mockMessageCatalog).
		Return(mockErrorFactory).
		Once()

	mockConfig.EXPECT().
		Get(expectedKey).
		Return(nil, messages.AnError).
		Once()

	mockErrorFactory.EXPECT().
		FromInternalError(messages.AnError).
		Return(expectedError).
		Once()

	adaptor := configadaptor.NewFactory(mockMessagesFactory).New(mockConfig, mockMessageCatalog)

	// Act
	result, err := adaptor.Get(expectedKey, "")

	// Assert
	require.ErrorIs(t, err, expectedError)
	require.Nil(t, result)
}

func TestConfig_Get_TypeMismatch(t *testing.T) {
	// Arrange
	mockConfig := &configmocks.MockInternalConfig{}
	defer mockConfig.AssertExpectations(t)

	mockMessageCatalog := &configmocks.MockInternalMessageCatalog{}
	defer mockMessageCatalog.AssertExpectations(t)

	mockMessagesFactory := &configmocks.MockMessagesFactory{}
	defer mockMessagesFactory.AssertExpectations(t)

	mockErrorFactory := &messagesmocks.MockI18nErrorFactory{}
	defer mockErrorFactory.AssertExpectations(t)

	expectedKey := "test-key"
	returnedValue := 123
	expectedInternalError := messages.New_StartupErrors_InvalidParameterType_Error(expectedKey, "string")
	expectedError := anI18nError

	mockMessagesFactory.EXPECT().
		New(mockMessageCatalog).
		Return(mockErrorFactory).
		Once()

	mockConfig.EXPECT().
		Get(expectedKey).
		Return(returnedValue, nil).
		Once()

	mockErrorFactory.EXPECT().
		FromInternalError(expectedInternalError).
		Return(expectedError).
		Once()

	adaptor := configadaptor.NewFactory(mockMessagesFactory).New(mockConfig, mockMessageCatalog)

	// Act
	result, err := adaptor.Get(expectedKey, "")

	// Assert
	require.ErrorIs(t, err, expectedError)
	require.Nil(t, result)
}

func TestConfig_Get_NilExpectedTypeZeroValue(t *testing.T) {
	// Arrange
	mockConfig := &configmocks.MockInternalConfig{}
	defer mockConfig.AssertExpectations(t)

	mockMessageCatalog := &configmocks.MockInternalMessageCatalog{}
	defer mockMessageCatalog.AssertExpectations(t)

	mockMessagesFactory := &configmocks.MockMessagesFactory{}
	defer mockMessagesFactory.AssertExpectations(t)

	mockErrorFactory := &messagesmocks.MockI18nErrorFactory{}
	defer mockErrorFactory.AssertExpectations(t)

	expectedKey := "test-key"
	returnedValue := "test-value"
	expectedInternalError := messages.New_StartupErrors_InvalidParameterType_Error(expectedKey, "<nil>")
	expectedError := anI18nError

	mockMessagesFactory.EXPECT().
		New(mockMessageCatalog).
		Return(mockErrorFactory).
		Once()

	mockConfig.EXPECT().
		Get(expectedKey).
		Return(returnedValue, nil).
		Once()

	mockErrorFactory.EXPECT().
		FromInternalError(expectedInternalError).
		Return(expectedError).
		Once()

	adaptor := configadaptor.NewFactory(mockMessagesFactory).New(mockConfig, mockMessageCatalog)

	// Act
	result, err := adaptor.Get(expectedKey, nil)

	// Assert
	require.ErrorIs(t, err, expectedError)
	require.Nil(t, result)
}

var anI18nError = &i18nError{} //nolint:gochecknoglobals // anI18nError is an error

type i18nError struct{}

func (e *i18nError) Error() string { return "" }

func (e *i18nError) MWMarker() {}
