// Copyright 2026 The MathWorks, Inc.

package config

import (
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/config"
	"github.com/matlab/matlab-mcp-server/pkg/i18n"
)

func Get[ParameterType supportedParameterValueType](cfg Config, parameter Parameter[ParameterType]) (ParameterType, i18n.Error) {
	return config.Get[ParameterType](cfg, parameter)
}
