// Copyright 2026 The MathWorks, Inc.

package main

import (
	"context"
	"os"

	"github.com/matlab/matlab-mcp-server/pkg/i18n"
	"github.com/matlab/matlab-mcp-server/pkg/server"
	"github.com/matlab/matlab-mcp-server/pkg/tools"
)

func main() {
	serverDefinition := server.Definition[Dependencies]{
		Name:         "server-with-custom-dependencies",
		Title:        "Server With Custom Dependencies",
		Instructions: "This is a test server with custom dependencies",

		DependenciesProvider: func(dependenciesProviderResources server.DependenciesProviderResources) (Dependencies, i18n.Error) {
			return DependenciesProvider(dependenciesProviderResources)
		},
		ToolsProvider: func(toolsProviderResources server.ToolsProviderResources[Dependencies]) []tools.Tool {
			return ToolsProvider(toolsProviderResources)
		},
	}
	serverInstance := server.New(serverDefinition)

	exitCode := serverInstance.StartAndWaitForCompletion(context.Background())

	os.Exit(exitCode)
}
