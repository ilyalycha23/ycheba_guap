// Copyright 2026 The MathWorks, Inc.

package main

import (
	"context"

	"github.com/matlab/matlab-mcp-server/pkg/i18n"
	"github.com/matlab/matlab-mcp-server/pkg/tools"
)

type GreetToolInput struct {
	Name string `json:"name"`
}

func NewGreetTool() tools.Tool {
	return tools.NewToolWithUnstructuredContentOutput(
		tools.NewDefinition(
			"greet",
			"Greet",
			"Greets a user by name",
			tools.NewReadOnlyAnnotations(),
		),
		func(ctx context.Context, request tools.CallRequest, inputs GreetToolInput) (tools.RichContent, i18n.Error) {
			return tools.RichContent{
				TextContent: []string{"Hello " + inputs.Name},
			}, nil
		},
	)
}
