// Copyright 2026 The MathWorks, Inc.

package adaptor

import (
	"github.com/matlab/matlab-mcp-server/internal/adaptors/application/definition"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/mcp/tools"
	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/wire"
)

type ApplicationDefinition interface {
	Name() string
	Title() string
	Instructions() string
	Features() definition.Features
	Parameters() []entities.Parameter
	Dependencies(resources definition.DependenciesProviderResources) (any, error)
	Tools(resources definition.ToolsProviderResources) []tools.Tool
}

type Application interface {
	ModeSelector() ModeSelector
	MessageCatalog() MessageCatalog
}

type ApplicationFactory interface {
	New(definition ApplicationDefinition) Application
}

type adaptorFactory struct{}

func NewFactory() ApplicationFactory {
	return &adaptorFactory{}
}

func (f *adaptorFactory) New(definition ApplicationDefinition) Application {
	return newAdaptor(wire.Initialize(definition))
}
