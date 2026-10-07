// Copyright 2026 The MathWorks, Inc.

package main

import (
	"github.com/matlab/matlab-mcp-server/pkg/logger"
	"github.com/matlab/matlab-mcp-server/pkg/tools"
)

type ToolsProviderResources interface {
	Logger() logger.Logger
	Dependencies() Dependencies
}

func ToolsProvider(resources ToolsProviderResources) []tools.Tool {
	resources.Logger().Info("Creating Tools")

	dataService := resources.Dependencies().DataService

	return []tools.Tool{
		NewGreetTool(dataService),
	}
}
