// Copyright 2026 The MathWorks, Inc.

package features

import (
	internaldefinition "github.com/matlab/matlab-mcp-server/internal/adaptors/application/definition"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
)

type Factory struct{}

func NewFactory() *Factory {
	return &Factory{}
}

func (f *Factory) New(features publictypes.Features) internaldefinition.Features {
	return internaldefinition.Features{
		MATLAB: internaldefinition.MATLABFeature{
			Enabled: features.MATLAB.Enabled,
		},
	}
}
