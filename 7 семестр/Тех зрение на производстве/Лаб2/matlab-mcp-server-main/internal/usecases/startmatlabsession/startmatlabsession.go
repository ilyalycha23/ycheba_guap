// Copyright 2025-2026 The MathWorks, Inc.

package startmatlabsession

import (
	"context"

	"github.com/matlab/matlab-mcp-server/internal/entities"
)

type Usecase struct {
	matlabManager entities.MATLABManager
}

type ReturnArgs struct {
	SessionID    entities.SessionID
	VerOutput    string
	AddOnsOutput string
}

func New(
	matlabManager entities.MATLABManager,
) *Usecase {
	return &Usecase{
		matlabManager: matlabManager,
	}
}

func (u *Usecase) Execute(ctx context.Context, sessionLogger entities.Logger, request entities.SessionDetails) (ReturnArgs, error) {
	sessionLogger.Debug("Entering StartMATLABSession Usecase")
	defer sessionLogger.Debug("Exiting StartMATLABSession Usecase")

	sessionID, err := u.matlabManager.StartMATLABSession(ctx, sessionLogger, request)
	if err != nil {
		return ReturnArgs{}, err
	}

	sessionLogger = sessionLogger.With("session_id", sessionID)

	sessionLogger.Debug("Getting the session client")
	client, err := u.matlabManager.GetMATLABSessionClient(ctx, sessionLogger, sessionID)
	if err != nil {
		return ReturnArgs{}, err
	}

	sessionLogger.Debug("Evaluating ver")
	verResponse, err := client.Eval(ctx, sessionLogger, entities.EvalRequest{Code: "ver"})
	if err != nil {
		return ReturnArgs{}, err
	}

	sessionLogger.Debug("Evaluating Add-Ons")
	AddOnsResponse, err := client.Eval(ctx, sessionLogger, entities.EvalRequest{Code: "matlab.addons.installedAddons()"})
	if err != nil {
		return ReturnArgs{}, err
	}

	return ReturnArgs{
		SessionID:    sessionID,
		VerOutput:    verResponse.ConsoleOutput,
		AddOnsOutput: AddOnsResponse.ConsoleOutput,
	}, nil
}
