// Copyright 2026 The MathWorks, Inc.

package main

import (
	"context"
	"os"

	"github.com/matlab/matlab-mcp-server/pkg/server"
	"github.com/matlab/matlab-mcp-server/pkg/tools"
)

func main() {
	serverDefinition := server.Definition[any]{
		Name:         "server-with-custom-tools",
		Title:        "Server With Custom Tools",
		Instructions: "This is a test server with custom tools",

		ToolsProvider: func(toolsProviderResources server.ToolsProviderResources[any]) []tools.Tool {
			return ToolsProvider(toolsProviderResources)
		},
	}
	serverInstance := server.New(serverDefinition)

	exitCode := serverInstance.StartAndWaitForCompletion(context.Background())

	os.Exit(exitCode)
}
