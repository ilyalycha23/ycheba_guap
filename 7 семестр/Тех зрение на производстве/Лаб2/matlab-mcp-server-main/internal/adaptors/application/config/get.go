// Copyright 2025-2026 The MathWorks, Inc.

package config

import (
	"reflect"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/application/parameter"
	"github.com/matlab/matlab-mcp-server/internal/messages"
)

func get[OutputType any](cfg GenericConfig, parameter *parameter.Parameter[OutputType]) (OutputType, messages.Error) {
	var zeroValue OutputType

	value, err := cfg.Get(parameter.GetID())
	if err != nil {
		return zeroValue, err
	}

	castValue, ok := value.(OutputType)
	if !ok {
		expectedType := reflect.TypeOf(zeroValue).String()
		return zeroValue, messages.New_StartupErrors_InvalidParameterType_Error(parameter.GetID(), expectedType)
	}

	return castValue, nil
}
