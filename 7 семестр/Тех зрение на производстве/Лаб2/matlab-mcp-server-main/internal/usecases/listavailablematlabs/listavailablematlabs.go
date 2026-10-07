// Copyright 2025-2026 The MathWorks, Inc.

package listavailablematlabs

import (
	"context"

	"github.com/matlab/matlab-mcp-server/internal/entities"
)

type Usecase struct {
	matlabManager entities.MATLABManager
}

type ReturnArgs []entities.EnvironmentInfo

func New(
	matlabManager entities.MATLABManager,
) *Usecase {
	return &Usecase{
		matlabManager: matlabManager,
	}
}

func (u *Usecase) Execute(ctx context.Context, sessionLogger entities.Logger) ReturnArgs {
	sessionLogger.Debug("Entering ListAvailableMATLABs Usecase")
	defer sessionLogger.Debug("Exiting ListAvailableMATLABs Usecase")

	return u.matlabManager.ListEnvironments(ctx, sessionLogger)
}
