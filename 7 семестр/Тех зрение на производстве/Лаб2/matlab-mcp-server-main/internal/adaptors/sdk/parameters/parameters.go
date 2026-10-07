// Copyright 2026 The MathWorks, Inc.

package parameters

import (
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
	internalentities "github.com/matlab/matlab-mcp-server/internal/entities"
)

type Factory struct{}

func NewFactory() *Factory {
	return &Factory{}
}

func (f *Factory) New(parameters []publictypes.Parameter) []internalentities.Parameter {
	if len(parameters) == 0 {
		return nil
	}

	internalParameters := make([]internalentities.Parameter, len(parameters))
	for i, parameter := range parameters {
		internalParameters[i] = parameter
	}

	return internalParameters
}
