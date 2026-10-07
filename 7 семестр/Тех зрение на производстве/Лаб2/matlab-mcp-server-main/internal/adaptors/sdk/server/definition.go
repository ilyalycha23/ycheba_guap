// Copyright 2026 The MathWorks, Inc.

package server

import (
	"slices"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
)

type Definition[Dependencies any] struct {
	Name         string
	Title        string
	Instructions string

	Features publictypes.Features

	Parameters []publictypes.Parameter

	DependenciesProvider publictypes.DependenciesProvider[Dependencies]

	ToolsProvider publictypes.ToolsProvider[Dependencies]
}

func NewDefinition[Dependencies any](
	name string,
	title string,
	instructions string,
	features publictypes.Features,
	parameters []publictypes.Parameter,
	dependenciesProvider publictypes.DependenciesProvider[Dependencies],
	toolsProvider publictypes.ToolsProvider[Dependencies],
) Definition[Dependencies] {
	return Definition[Dependencies]{
		Name:         name,
		Title:        title,
		Instructions: instructions,

		Features: features,

		Parameters: slices.Clone(parameters),

		DependenciesProvider: dependenciesProvider,

		ToolsProvider: toolsProvider,
	}
}
