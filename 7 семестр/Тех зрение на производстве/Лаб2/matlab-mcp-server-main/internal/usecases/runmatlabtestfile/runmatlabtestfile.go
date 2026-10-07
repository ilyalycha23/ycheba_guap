// Copyright 2025-2026 The MathWorks, Inc.

package runmatlabtestfile

import (
	"context"
	"fmt"

	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/usecases/utils/matlabstring"
)

type Args struct {
	ScriptPath string
}

type PathValidator interface {
	ValidateMATLABScript(filePath string) (string, error)
}

type Usecase struct {
	pathValidator PathValidator
}

func New(
	pathValidator PathValidator,
) *Usecase {
	return &Usecase{
		pathValidator: pathValidator,
	}
}

func (u *Usecase) Execute(ctx context.Context, sessionLogger entities.Logger, client entities.MATLABSessionClient, request Args) (entities.EvalResponse, error) {
	sessionLogger.Debug("Entering RunMATLABTestFile Usecase")
	defer sessionLogger.Debug("Exiting RunMATLABTestFile Usecase")

	validatedPath, err := u.pathValidator.ValidateMATLABScript(request.ScriptPath)
	if err != nil {
		return entities.EvalResponse{}, err
	}

	runCodeRequest := entities.EvalRequest{
		Code: fmt.Sprintf("runtests('%s')", matlabstring.EscapeSingleQuotes(validatedPath)),
	}

	response, err := client.EvalWithCapture(ctx, sessionLogger, runCodeRequest)
	if err != nil {
		return entities.EvalResponse{}, err
	}

	return entities.EvalResponse{
		ConsoleOutput: response.ConsoleOutput,
	}, nil
}
