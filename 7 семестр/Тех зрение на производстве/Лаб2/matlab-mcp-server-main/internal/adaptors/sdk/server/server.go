// Copyright 2026 The MathWorks, Inc.

package server

import (
	"context"
	"fmt"

	internaldefinition "github.com/matlab/matlab-mcp-server/internal/adaptors/application/definition"
	publictypes "github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/toolsprovider"
	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/wire/adaptor"
)

type DependenciesProviderFactory[Dependencies any] interface {
	New(provider publictypes.DependenciesProvider[Dependencies]) internaldefinition.DependenciesProvider
}

type ToolsProviderFactory[Dependencies any] interface {
	New(provider toolsprovider.ToolsProvider[Dependencies]) internaldefinition.ToolsProvider
}

type ParametersFactory interface {
	New(parameters []publictypes.Parameter) []entities.Parameter
}

type FeaturesFactory interface {
	New(features publictypes.Features) internaldefinition.Features
}

type ApplicationFactory interface {
	New(definition adaptor.ApplicationDefinition) adaptor.Application
}

type Server[Dependencies any] struct {
	serverDefinition            Definition[Dependencies]
	featuresFactory             FeaturesFactory
	parametersFactory           ParametersFactory
	dependenciesProviderFactory DependenciesProviderFactory[Dependencies]
	toolsProviderFactory        ToolsProviderFactory[Dependencies]
	applicationFactory          ApplicationFactory
	errorWriter                 entities.Writer
}

func New[Dependencies any](
	serverDefinition Definition[Dependencies],
	featuresFactory FeaturesFactory,
	parametersFactory ParametersFactory,
	dependenciesProviderFactory DependenciesProviderFactory[Dependencies],
	toolsProviderFactory ToolsProviderFactory[Dependencies],
	applicationFactory ApplicationFactory,
	errorWriter entities.Writer,
) *Server[Dependencies] {
	return &Server[Dependencies]{
		serverDefinition:            serverDefinition,
		featuresFactory:             featuresFactory,
		parametersFactory:           parametersFactory,
		dependenciesProviderFactory: dependenciesProviderFactory,
		toolsProviderFactory:        toolsProviderFactory,
		applicationFactory:          applicationFactory,
		errorWriter:                 errorWriter,
	}
}

func (s *Server[Dependencies]) StartAndWaitForCompletion(ctx context.Context) int {
	serverDefinition := internaldefinition.New(
		s.serverDefinition.Name,
		s.serverDefinition.Title,
		s.serverDefinition.Instructions,
		s.featuresFactory.New(
			s.serverDefinition.Features,
		),
		s.parametersFactory.New(
			s.serverDefinition.Parameters,
		),
		s.dependenciesProviderFactory.New(
			s.serverDefinition.DependenciesProvider,
		),
		s.toolsProviderFactory.New(
			s.serverDefinition.ToolsProvider,
		),
	)

	application := s.applicationFactory.New(serverDefinition)

	if err := application.ModeSelector().StartAndWaitForCompletion(ctx); err != nil {
		messageCatalog := application.MessageCatalog()
		errorMessage := messageCatalog.GetFromError(err)
		fmt.Fprintf(s.errorWriter, "%s\n", errorMessage) //nolint:errcheck // Nothing we can do then
		return 1
	}

	return 0
}
