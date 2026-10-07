// Copyright 2026 The MathWorks, Inc.

package main

import (
	"github.com/matlab/matlab-mcp-server/pkg/logger"
	"github.com/matlab/matlab-mcp-server/pkg/tools"
)

type ToolsProviderResources interface { //nolint:iface // Same interface is happenstance
	Logger() logger.Logger
}

func ToolsProvider(resources ToolsProviderResources) []tools.Tool {
	resources.Logger().Info("Creating Tools")

	return []tools.Tool{
		NewToolThatLogs(),
		NewStructuredToolThatLogs(),
	}
}
