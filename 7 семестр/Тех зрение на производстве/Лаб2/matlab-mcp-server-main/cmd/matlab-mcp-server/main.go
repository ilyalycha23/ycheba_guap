// Copyright 2025-2026 The MathWorks, Inc.

package main

import (
	"context"
	"os"

	"github.com/matlab/matlab-mcp-server/pkg/server"

	_ "embed"
)

//go:embed assets/instructions.txt
var instructions string

func main() {
	serverDefinition := server.Definition[any]{
		Name:         "matlab-mcp-server",
		Title:        "MATLAB MCP Server",
		Instructions: instructions,

		Features: server.Features{
			MATLAB: server.MATLABFeature{
				Enabled: true,
			},
		},
	}
	serverInstance := server.New(serverDefinition)

	ctx := context.Background()
	exitCode := serverInstance.StartAndWaitForCompletion(ctx)

	os.Exit(exitCode)
}
