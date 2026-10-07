// Copyright 2026 The MathWorks, Inc.

package toolsproviderresources

import (
	"github.com/matlab/matlab-mcp-server/internal/adaptors/application/definition"
	publictypes "github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
	"github.com/matlab/matlab-mcp-server/internal/entities"
)

type LoggerFactory interface {
	New(logger entities.Logger) publictypes.Logger
}

type Factory[Dependencies any] struct {
	loggerFactory LoggerFactory
}

func NewFactory[Dependencies any](
	loggerFactory LoggerFactory,
) *Factory[Dependencies] {
	return &Factory[Dependencies]{
		loggerFactory: loggerFactory,
	}
}

func (f *Factory[Dependencies]) New(
	internal definition.ToolsProviderResources,
) publictypes.ToolsProviderResources[Dependencies] {
	var dependencies Dependencies
	if internal.Dependencies == nil {
		return &toolsProviderResourcesAdaptor[Dependencies]{
			logger:       f.loggerFactory.New(internal.Logger),
			dependencies: dependencies,
		}
	}
	castDependencies, ok := internal.Dependencies.(Dependencies)
	if ok {
		dependencies = castDependencies
	} else {
		internal.Logger.Error("Dependencies type cast failed, using zero value")
	}

	return &toolsProviderResourcesAdaptor[Dependencies]{
		logger:       f.loggerFactory.New(internal.Logger),
		dependencies: dependencies,
	}
}

type toolsProviderResourcesAdaptor[Dependencies any] struct {
	logger       publictypes.Logger
	dependencies Dependencies
}

func (r *toolsProviderResourcesAdaptor[Dependencies]) Logger() publictypes.Logger {
	return r.logger
}

func (r *toolsProviderResourcesAdaptor[Dependencies]) Dependencies() Dependencies {
	return r.dependencies
}
