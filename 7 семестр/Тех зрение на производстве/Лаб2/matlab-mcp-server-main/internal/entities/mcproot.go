// Copyright 2026 The MathWorks, Inc.

package entities

// MCPRoot represents an MCP root as a pure domain data structure.
type MCPRoot struct {
	uri  string
	name string
}

func NewMCPRoot(uri, name string) MCPRoot {
	return MCPRoot{uri: uri, name: name}
}

func (r MCPRoot) URI() string {
	return r.uri
}

func (r MCPRoot) Name() string {
	return r.name
}
