// Copyright 2026 The MathWorks, Inc.

package adaptor

import (
	"github.com/matlab/matlab-mcp-server/internal/wire"
)

// NewAdaptor exposes the internal adaptor constructor for testing purposes.
func NewAdaptor(app *wire.Application) *adaptor {
	return newAdaptor(app)
}
