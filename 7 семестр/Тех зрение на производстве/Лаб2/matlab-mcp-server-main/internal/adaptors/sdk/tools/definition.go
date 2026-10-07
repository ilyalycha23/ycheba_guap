// Copyright 2026 The MathWorks, Inc.

package tools

import "github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"

func NewDefinition(name, title, description string, annotations publictypes.Annotations) publictypes.ToolDefinition {
	if annotations == nil {
		annotations = newDefaultAnnotation()
	}

	return publictypes.ToolDefinition{
		Name:        name,
		Title:       title,
		Description: description,
		Annotations: annotations,
	}
}
