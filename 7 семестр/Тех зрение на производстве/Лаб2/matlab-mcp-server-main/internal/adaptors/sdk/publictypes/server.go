// Copyright 2026 The MathWorks, Inc.

package publictypes

import "context"

type Server interface {
	StartAndWaitForCompletion(ctx context.Context) int
}
