// Copyright 2025-2026 The MathWorks, Inc.

package config

import (
	"github.com/matlab/matlab-mcp-server/internal/adaptors/application/parameter"
	"github.com/matlab/matlab-mcp-server/internal/messages"
)

func Get[OutputType any](cfg GenericConfig, parameter *parameter.Parameter[OutputType]) (OutputType, messages.Error) {
	return get(cfg, parameter)
}
