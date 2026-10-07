// Copyright 2025-2026 The MathWorks, Inc.

package matlabmanager

import (
	"context"

	"github.com/matlab/matlab-mcp-server/internal/entities"
)

func (m *MATLABManager) StopMATLABSession(ctx context.Context, sessionLogger entities.Logger, sessionID entities.SessionID) error {
	client, err := m.sessionStore.Get(sessionID)
	if err != nil {
		return err
	}

	defer m.sessionStore.Remove(sessionID)

	return client.StopSession(ctx, sessionLogger.With("session-id", sessionID))
}
