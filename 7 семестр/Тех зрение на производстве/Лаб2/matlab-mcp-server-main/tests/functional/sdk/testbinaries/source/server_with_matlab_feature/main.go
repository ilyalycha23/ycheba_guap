// Copyright 2026 The MathWorks, Inc.

package main

import (
	"context"
	"os"

	"github.com/matlab/matlab-mcp-server/pkg/server"
)

func main() {
	serverDefinition := server.Definition[any]{
		Name:         "server-with-matlab-feature",
		Title:        "Server With MATLAB Feature",
		Instructions: "This is a test server with MATLAB feature",

		Features: server.Features{
			MATLAB: server.MATLABFeature{
				Enabled: true,
			},
		},
	}
	serverInstance := server.New(serverDefinition)

	exitCode := serverInstance.StartAndWaitForCompletion(context.Background())

	os.Exit(exitCode)
}
