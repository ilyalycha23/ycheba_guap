// Copyright 2026 The MathWorks, Inc.

package main

import (
	"github.com/matlab/matlab-mcp-server/pkg/tools"
)

type ToolsProviderResources interface{}

func ToolsProvider(resources ToolsProviderResources) []tools.Tool {
	return []tools.Tool{
		NewGreetTool(),
		NewGreetStructuredTool(),
	}
}
