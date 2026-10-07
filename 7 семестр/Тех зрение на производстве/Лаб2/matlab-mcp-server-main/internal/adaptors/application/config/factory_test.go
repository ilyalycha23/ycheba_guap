// Copyright 2025-2026 The MathWorks, Inc.

package config_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/application/config"
	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/messages"
	configmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/application/config"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestNewFactory_HappyPath(t *testing.T) {
	// Arrange
	mockOSLayer := &configmocks.MockOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockParser := &configmocks.MockParser{}
	defer mockParser.AssertExpectations(t)

	mockBuildInfo := &configmocks.MockBuildInfo{}
	defer mockBuildInfo.AssertExpectations(t)

	// Act
	factory := config.NewFactory(mockParser, mockOSLayer, mockBuildInfo)

	// Assert
	assert.NotNil(t, factory, "Factory should not be nil")
}

func TestFactory_Config_HappyPath(t *testing.T) {
	// Arrange
	mockOSLayer := &configmocks.MockOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockParser := &configmocks.MockParser{}
	defer mockParser.AssertExpectations(t)

	mockBuildInfo := &configmocks.MockBuildInfo{}
	defer mockBuildInfo.AssertExpectations(t)

	programName := "testprocess"
	args := []string{programName}

	mockOSLayer.EXPECT().
		Args().
		Return(args).
		Once()

	mockParser.EXPECT().
		Parse(args[1:]).
		Return([]entities.Parameter{}, configDefaultParsedArgs(), []string{}, nil).
		Once()

	factory := config.NewFactory(mockParser, mockOSLayer, mockBuildInfo)

	// Act
	cfg, err := factory.Config()

	// Assert
	require.NoError(t, err, "Config should not return an error")
	assert.NotNil(t, cfg, "Config should not be nil")
}

func TestFactory_Config_IsSingleton(t *testing.T) {
	// Arrange
	mockOSLayer := &configmocks.MockOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockParser := &configmocks.MockParser{}
	defer mockParser.AssertExpectations(t)

	mockBuildInfo := &configmocks.MockBuildInfo{}
	defer mockBuildInfo.AssertExpectations(t)

	programName := "testprocess"
	args := []string{programName}

	mockOSLayer.EXPECT().
		Args().
		Return(args).
		Once()

	mockParser.EXPECT().
		Parse(args[1:]).
		Return([]entities.Parameter{}, configDefaultParsedArgs(), []string{}, nil).
		Once()

	factory := config.NewFactory(mockParser, mockOSLayer, mockBuildInfo)

	// Act
	cfg1, err1 := factory.Config()
	cfg2, err2 := factory.Config()

	// Assert
	require.NoError(t, err1, "First Config call should not return an error")
	require.NoError(t, err2, "Second Config call should not return an error")
	assert.Same(t, cfg1, cfg2, "Config should return the same instance on multiple calls")
}

func TestFactory_Config_SingletonPreservesError(t *testing.T) {
	// Arrange
	mockOSLayer := &configmocks.MockOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockParser := &configmocks.MockParser{}
	defer mockParser.AssertExpectations(t)

	mockBuildInfo := &configmocks.MockBuildInfo{}
	defer mockBuildInfo.AssertExpectations(t)

	programName := "testprocess"
	args := []string{programName}

	mockOSLayer.EXPECT().
		Args().
		Return(args).
		Once()

	mockParser.EXPECT().
		Parse(args[1:]).
		Return(nil, nil, nil, messages.AnError).
		Once()

	factory := config.NewFactory(mockParser, mockOSLayer, mockBuildInfo)

	// Act
	cfg1, err1 := factory.Config()
	cfg2, err2 := factory.Config()

	// Assert
	require.ErrorIs(t, err1, messages.AnError, "First Config call should return an error")
	require.ErrorIs(t, err2, messages.AnError, "Second Config call should return the same error")
	assert.Nil(t, cfg1, "First config should be nil")
	assert.Nil(t, cfg2, "Second config should be nil")
}
