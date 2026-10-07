// Copyright 2026 The MathWorks, Inc.

package publictypes

type Config interface {
	Get(key string, expectedType any) (any, Error)
}
