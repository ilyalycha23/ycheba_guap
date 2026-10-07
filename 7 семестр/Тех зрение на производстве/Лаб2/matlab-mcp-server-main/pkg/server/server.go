// Copyright 2026 The MathWorks, Inc.

package server

import (
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/server"
)

type Definition[Dependencies any] struct {
	Name         string
	Title        string
	Instructions string

	Features Features

	Parameters []Parameter

	DependenciesProvider DependenciesProvider[Dependencies]

	ToolsProvider ToolsProvider[Dependencies]
}

type Server = publictypes.Server

func New[Dependencies any](thisDefinition Definition[Dependencies]) Server {
	internalDefinition := server.NewDefinition(
		thisDefinition.Name,
		thisDefinition.Title,
		thisDefinition.Instructions,
		thisDefinition.Features,
		thisDefinition.Parameters,
		thisDefinition.DependenciesProvider,
		thisDefinition.ToolsProvider,
	)
	return sdk.NewServer(internalDefinition)
}
