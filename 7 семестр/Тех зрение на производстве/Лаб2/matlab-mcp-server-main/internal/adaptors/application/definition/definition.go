// Copyright 2026 The MathWorks, Inc.

package definition

import (
	"github.com/matlab/matlab-mcp-server/internal/adaptors/mcp/tools"
	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/messages"
)

type MessageCatalog interface {
	GetFromError(err messages.Error) string
}

type Definition struct {
	name         string
	title        string
	instructions string

	features Features

	parameters []entities.Parameter

	dependenciesProvider DependenciesProvider

	toolsProvider ToolsProvider
}

func New(
	name string,
	title string,
	instructions string,
	features Features,
	parameters []entities.Parameter,
	dependenciesProvider DependenciesProvider,
	toolsProvider ToolsProvider,
) Definition {
	return Definition{
		name:         name,
		title:        title,
		instructions: instructions,

		features: features,

		parameters: parameters,

		dependenciesProvider: dependenciesProvider,

		toolsProvider: toolsProvider,
	}
}

func (d Definition) Name() string {
	return d.name
}

func (d Definition) Title() string {
	return d.title
}

func (d Definition) Instructions() string {
	return d.instructions
}

func (d Definition) Features() Features {
	return d.features
}

func (d Definition) Parameters() []entities.Parameter {
	return d.parameters
}

func (d Definition) Dependencies(resources DependenciesProviderResources) (any, error) {
	if d.dependenciesProvider == nil {
		return nil, nil
	}

	return d.dependenciesProvider(resources)
}

func (d Definition) Tools(resources ToolsProviderResources) []tools.Tool {
	if d.toolsProvider == nil {
		return nil
	}

	return d.toolsProvider(resources)
}
