// Copyright 2026 The MathWorks, Inc.

package main

import (
	"context"

	"github.com/matlab/matlab-mcp-server/pkg/i18n"
	"github.com/matlab/matlab-mcp-server/pkg/tools"
)

type GetPIDInput struct{}

type GetPIDOutput struct {
	PID int `json:"pid"`
}

// NewGetPIDTool is contrived way of getting the PID to the test point.
func NewGetPIDTool(pid int) tools.Tool {
	return tools.NewToolWithStructuredContentOutput(
		tools.NewDefinition(
			"get-pid",
			"Get PID",
			"Returns the PID of the watched child process",
			tools.NewReadOnlyAnnotations(),
		),
		func(ctx context.Context, request tools.CallRequest, inputs GetPIDInput) (GetPIDOutput, i18n.Error) {
			return GetPIDOutput{
				PID: pid,
			}, nil
		},
	)
}
