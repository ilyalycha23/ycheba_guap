// Copyright 2026 The MathWorks, Inc.

package globalmatlab

import (
	"github.com/matlab/matlab-mcp-server/internal/entities"
)

func (g *GlobalMATLAB) SetSessionIDForTesting(sessionID entities.SessionID) {
	g.lock.Lock()
	defer g.lock.Unlock()
	g.sessionID = sessionID
}
