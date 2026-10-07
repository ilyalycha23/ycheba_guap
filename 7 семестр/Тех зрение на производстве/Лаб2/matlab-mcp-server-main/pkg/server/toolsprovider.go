// Copyright 2026 The MathWorks, Inc.

package server

import (
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
)

type ToolsProviderResources[Dependencies any] = publictypes.ToolsProviderResources[Dependencies]

type ToolsProvider[Dependencies any] = publictypes.ToolsProvider[Dependencies]
