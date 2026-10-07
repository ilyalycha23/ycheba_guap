// Copyright 2026 The MathWorks, Inc.

package matlabmanager

import (
	"context"
	"strings"

	"github.com/matlab/matlab-mcp-server/internal/entities"
)

// try/catch suppresses red error text in an attached desktop when the
// target function is missing.
const correlationIDRetrievalCode = `` +
	`try, ` +
	`disp(matlab.internal.serviceprocess.getClientId().id); ` +
	`catch, ` +
	`end`

func retrieveCorrelationID(ctx context.Context, sessionLogger entities.Logger, client entities.MATLABSessionClient) string {
	response, err := client.Eval(ctx, sessionLogger, entities.EvalRequest{
		Code: correlationIDRetrievalCode,
	})
	if err != nil {
		return ""
	}
	return strings.TrimSpace(response.ConsoleOutput)
}
