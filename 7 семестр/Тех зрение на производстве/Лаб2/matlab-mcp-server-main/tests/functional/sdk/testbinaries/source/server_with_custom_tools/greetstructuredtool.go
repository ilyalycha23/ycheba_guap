// Copyright 2026 The MathWorks, Inc.

package main

import (
	"context"

	"github.com/matlab/matlab-mcp-server/pkg/i18n"
	"github.com/matlab/matlab-mcp-server/pkg/tools"
)

type GreetStructuredToolInput struct {
	Name string `json:"name"`
}

type GreetStructuredToolOutput struct {
	Response string `json:"response"`
}

func NewGreetStructuredTool() tools.Tool {
	return tools.NewToolWithStructuredContentOutput(
		tools.NewDefinition(
			"greet-structured",
			"Greet (Structured Content Output)",
			"Greets a user by name (Structured Content Output)",
			tools.NewReadOnlyAnnotations(),
		),
		func(ctx context.Context, request tools.CallRequest, inputs GreetStructuredToolInput) (GreetStructuredToolOutput, i18n.Error) {
			return GreetStructuredToolOutput{
				Response: "Hello " + inputs.Name,
			}, nil
		},
	)
}
