// Copyright 2026 The MathWorks, Inc.

package main

import (
	"context"
	"os"
	"os/signal"
	"syscall"

	"github.com/matlab/matlab-mcp-server/pkg/i18n"
	"github.com/matlab/matlab-mcp-server/pkg/server"
	"github.com/matlab/matlab-mcp-server/pkg/tools"
)

func main() {
	// This is purely for convenience, for cross-platform tests.
	// ./childprocess.go for an explanation.
	if os.Getenv(childProcessEnvVar) == "1" {
		interruptC := make(chan os.Signal, 1)
		signal.Notify(interruptC, os.Interrupt, syscall.SIGTERM)
		<-interruptC
		return
	}

	serverDefinition := server.Definition[Dependencies]{
		Name:         "server-with-watchdog",
		Title:        "Server With Watchdog",
		Instructions: "This is a test server with watchdog",

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
