// Copyright 2025 The MathWorks, Inc.

package basetool

func (t *tool[ToolInput, ToolOutput]) SetToolAdder(toolAdder ToolAdder[ToolInput, ToolOutput]) {
	t.toolAdder = toolAdder
}
