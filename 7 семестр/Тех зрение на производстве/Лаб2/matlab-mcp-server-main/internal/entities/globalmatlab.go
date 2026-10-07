// Copyright 2025 The MathWorks, Inc.

package entities

import "context"

type GlobalMATLAB interface {
	Client(ctx context.Context, logger Logger) (MATLABSessionClient, error)
}
