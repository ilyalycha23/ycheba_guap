// Copyright 2025-2026 The MathWorks, Inc.

package detectmatlabtoolboxes

import (
	"context"

	"github.com/matlab/matlab-mcp-server/internal/entities"
)

type Usecase struct {
}

func New() *Usecase {
	return &Usecase{}
}

type ReturnArgs struct {
	Toolboxes string
}

func (u *Usecase) Execute(ctx context.Context, sessionLogger entities.Logger, client entities.MATLABSessionClient) (ReturnArgs, error) {
	sessionLogger.Debug("Entering DetectMATLABToolboxes Usecase")
	defer sessionLogger.Debug("Exiting DetectMATLABToolboxes Usecase")

	verRequest := entities.EvalRequest{
		Code: "ver",
	}

	ver, err := client.Eval(ctx, sessionLogger, verRequest)
	if err != nil {
		return ReturnArgs{}, err
	}

	return ReturnArgs{
		Toolboxes: ver.ConsoleOutput,
	}, nil
}
