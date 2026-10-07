// Copyright 2026 The MathWorks, Inc.

package tools

import (
	"context"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/tools"
	"github.com/matlab/matlab-mcp-server/pkg/i18n"
)

type Definition = publictypes.ToolDefinition

func NewDefinition(name, title, description string, annotations Annotations) Definition {
	return tools.NewDefinition(name, title, description, annotations)
}

type Tool = publictypes.Tool

type CallRequest = publictypes.ToolCallRequest

type RichContent = publictypes.RichContent

type HandlerForToolWithUnstructuredContentOutput[ToolInput any] func(ctx context.Context, request CallRequest, inputs ToolInput) (RichContent, i18n.Error)

func NewToolWithUnstructuredContentOutput[ToolInput any](definition Definition, handler HandlerForToolWithUnstructuredContentOutput[ToolInput]) Tool {
	return tools.NewUnstructured(definition, tools.UnstructuredHandler[ToolInput](handler))
}

type HandlerForToolWithStructuredContentOutput[ToolInput, ToolOutput any] func(ctx context.Context, request CallRequest, inputs ToolInput) (ToolOutput, i18n.Error)

func NewToolWithStructuredContentOutput[ToolInput, ToolOutput any](definition Definition, handler HandlerForToolWithStructuredContentOutput[ToolInput, ToolOutput]) Tool {
	return tools.NewStructured(definition, tools.StructuredHandler[ToolInput, ToolOutput](handler))
}
