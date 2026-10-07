// Copyright 2026 The MathWorks, Inc.

package dependenciesprovider

import (
	"github.com/matlab/matlab-mcp-server/internal/adaptors/application/definition"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
)

type ResourcesFactory interface {
	New(internal definition.DependenciesProviderResources) publictypes.DependenciesProviderResources
}

type Factory[Dependencies any] struct {
	resourcesFactory ResourcesFactory
}

func NewFactory[Dependencies any](
	resourcesFactory ResourcesFactory,
) *Factory[Dependencies] {
	return &Factory[Dependencies]{
		resourcesFactory: resourcesFactory,
	}
}

func (f *Factory[Dependencies]) New(provider publictypes.DependenciesProvider[Dependencies]) definition.DependenciesProvider {
	return func(internalResources definition.DependenciesProviderResources) (any, error) {
		if provider == nil {
			return nil, nil
		}

		resources := f.resourcesFactory.New(internalResources)
		dependencies, err := provider(resources)
		if err != nil {
			return nil, err
		}

		return dependencies, nil
	}
}
