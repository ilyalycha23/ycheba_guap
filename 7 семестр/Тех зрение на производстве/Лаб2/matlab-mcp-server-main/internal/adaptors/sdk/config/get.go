// Copyright 2026 The MathWorks, Inc.

package config

import (
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
)

type SupportedParameterValueType interface {
	string | bool
}

type parameter[ParameterType SupportedParameterValueType] interface {
	GetID() string
}

func Get[ParameterType SupportedParameterValueType](cfg publictypes.Config, parameter parameter[ParameterType]) (ParameterType, publictypes.Error) {
	var zeroValue ParameterType

	value, err := cfg.Get(parameter.GetID(), zeroValue)
	if err != nil {
		return zeroValue, err
	}

	castValue, ok := value.(ParameterType)
	if !ok {
		// This code path should be unreachable.
		// cfg.Get is expected to error on type mismatch.
		return zeroValue, nil
	}

	return castValue, nil
}
