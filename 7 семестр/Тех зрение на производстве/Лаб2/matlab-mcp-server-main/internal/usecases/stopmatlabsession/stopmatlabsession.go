// Copyright 2025-2026 The MathWorks, Inc.

package stopmatlabsession

import (
	"context"

	"github.com/matlab/matlab-mcp-server/internal/entities"
)

type Usecase struct {
	matlabManager entities.MATLABManager
}

func New(
	matlabManager entities.MATLABManager,
) *Usecase {
	return &Usecase{
		matlabManager: matlabManager,
	}
}

func (u *Usecase) Execute(ctx context.Context, sessionLogger entities.Logger, sessionID entities.SessionID) error {
	sessionLogger = sessionLogger.With("session_id", sessionID)
	sessionLogger.Debug("Entering StopMATLABSession Usecase")
	defer sessionLogger.Debug("Exiting StopMATLABSession Usecase")

	return u.matlabManager.StopMATLABSession(ctx, sessionLogger, sessionID)
}
