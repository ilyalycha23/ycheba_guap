// Copyright 2026 The MathWorks, Inc.

package server

import (
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
)

type DependenciesProviderResources = publictypes.DependenciesProviderResources

type DependenciesProvider[Dependencies any] = publictypes.DependenciesProvider[Dependencies]
