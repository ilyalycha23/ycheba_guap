// Copyright 2026 The MathWorks, Inc.

package publictypes

type Annotations interface {
	mwAnnotationSeal()
}

type ToolDefinition struct {
	Name        string
	Title       string
	Description string
	Annotations Annotations
}

type Tool interface {
	mwToolSeal()
}

type ToolsProviderResources[Dependencies any] interface {
	Logger() Logger
	Dependencies() Dependencies
}

type ToolsProvider[Dependencies any] func(ToolsProviderResources[Dependencies]) []Tool

type ToolCallRequest interface {
	Logger() Logger
	Config() Config
}

type RichContent struct {
	TextContent []string
}

// Nifty little trick to create cross-package seals
// Any struct that embed this will match the Tool interface
// However, because it is in `internal`, it keeps the seal private
type ToolSeal struct{}

func (s ToolSeal) mwToolSeal() {}

type AnnotationSeal struct{}

func (s AnnotationSeal) mwAnnotationSeal() {}
