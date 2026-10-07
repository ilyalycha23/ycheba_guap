// Copyright 2026 The MathWorks, Inc.

package matlabmanager

import (
	"github.com/matlab/matlab-mcp-server/internal/entities"
)

func (m *MATLABManager) GetSessionCorrelationID(sessionID entities.SessionID) string {
	return m.sessionStore.CorrelationID(sessionID)
}
