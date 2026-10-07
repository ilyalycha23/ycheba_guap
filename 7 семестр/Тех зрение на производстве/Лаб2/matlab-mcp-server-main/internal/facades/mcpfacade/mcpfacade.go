// Copyright 2025 The MathWorks, Inc.

package mcpfacade

import "github.com/modelcontextprotocol/go-sdk/mcp"

type ToolAdder[ToolInput, ToolOutput any] struct {
}

func NewToolAdder[ToolInput, ToolOutput any]() *ToolAdder[ToolInput, ToolOutput] {
	return &ToolAdder[ToolInput, ToolOutput]{}
}

func (*ToolAdder[ToolInput, ToolOutput]) AddTool(server *mcp.Server, tool *mcp.Tool, handler mcp.ToolHandlerFor[ToolInput, ToolOutput]) {
	mcp.AddTool(server, tool, handler)
}
