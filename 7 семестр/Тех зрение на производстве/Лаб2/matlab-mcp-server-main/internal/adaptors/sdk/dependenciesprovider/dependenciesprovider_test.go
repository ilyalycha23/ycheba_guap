// Copyright 2026 The MathWorks, Inc.

package dependenciesprovider_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/application/definition"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/dependenciesprovider"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
	"github.com/matlab/matlab-mcp-server/internal/testutils"
	dependenciesprovidermocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/sdk/dependenciesprovider"
	publictypesmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/sdk/publictypes"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestNewFactory_HappyPath(t *testing.T) {
	// Arrange
	mockResourcesFactory := &dependenciesprovidermocks.MockResourcesFactory{}
	defer mockResourcesFactory.AssertExpectations(t)

	// Act
	factory := dependenciesprovider.NewFactory[struct{}](mockResourcesFactory)

	// Assert
	require.NotNil(t, factory)
}

func TestFactory_New_HappyPath(t *testing.T) {
	// Arrange
	mockResourcesFactory := &dependenciesprovidermocks.MockResourcesFactory{}
	defer mockResourcesFactory.AssertExpectations(t)

	mockResources := &publictypesmocks.MockDependenciesProviderResources{}
	defer mockResources.AssertExpectations(t)

	type TestDependencies struct{}
	expectedDependencies := &TestDependencies{}
	expectedInternalResources := definition.DependenciesProviderResources{
		Logger: testutils.NewInspectableLogger(),
	}

	mockResourcesFactory.EXPECT().
		New(expectedInternalResources).
		Return(mockResources).
		Once()

	provider := publictypes.DependenciesProvider[*TestDependencies](func(resources publictypes.DependenciesProviderResources) (*TestDependencies, publictypes.Error) {
		assert.Equal(t, mockResources, resources)
		return expectedDependencies, nil
	})

	// Act
	internalProvider := dependenciesprovider.NewFactory[*TestDependencies](mockResourcesFactory).New(provider)
	dependencies, err := internalProvider(expectedInternalResources)

	// Assert
	require.NoError(t, err)
	require.Equal(t, expectedDependencies, dependencies)
}

func TestFactory_New_NilProvider(t *testing.T) {
	// Arrange
	mockResourcesFactory := &dependenciesprovidermocks.MockResourcesFactory{}
	defer mockResourcesFactory.AssertExpectations(t)

	// Act
	internalProvider := dependenciesprovider.NewFactory[struct{}](mockResourcesFactory).New(nil)
	result, err := internalProvider(definition.DependenciesProviderResources{})

	// Assert
	require.NoError(t, err)
	require.Nil(t, result)
}

func TestFactory_New_Error(t *testing.T) {
	// Arrange
	mockResourcesFactory := &dependenciesprovidermocks.MockResourcesFactory{}
	defer mockResourcesFactory.AssertExpectations(t)

	mockResources := &publictypesmocks.MockDependenciesProviderResources{}
	defer mockResources.AssertExpectations(t)

	type TestDependencies struct{}
	expectedError := anI18nError
	expectedInternalResources := definition.DependenciesProviderResources{
		Logger: testutils.NewInspectableLogger(),
	}

	mockResourcesFactory.EXPECT().
		New(expectedInternalResources).
		Return(mockResources).
		Once()

	provider := publictypes.DependenciesProvider[*TestDependencies](func(resources publictypes.DependenciesProviderResources) (*TestDependencies, publictypes.Error) {
		return &TestDependencies{}, expectedError
	})

	// Act
	internalProvider := dependenciesprovider.NewFactory[*TestDependencies](mockResourcesFactory).New(provider)
	dependencies, err := internalProvider(expectedInternalResources)

	// Assert
	require.ErrorIs(t, err, expectedError)
	require.Nil(t, dependencies)
}

var anI18nError = &i18nError{} //nolint:gochecknoglobals // anI18nError is an error

type i18nError struct{}

func (e *i18nError) Error() string { return "" }

func (e *i18nError) MWMarker() {}
