// Copyright 2026 The MathWorks, Inc.

// mcpb-gen stages MCPB bundle artifacts for packaging.
// Must be built then executed (not "go run") because runtime/debug.ReadBuildInfo()
// only returns a proper version from a compiled binary.
package main

import (
	"fmt"
	"os"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/buildinfo"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/mcpb/mcpbstagebuilder"
	"github.com/matlab/matlab-mcp-server/internal/facades/osfacade"
)

func main() {
	osFacade := osfacade.New()
	buildInfoAdaptor := buildinfo.New(osFacade)
	version := buildInfoAdaptor.Version()

	if err := mcpbstagebuilder.Build(version); err != nil {
		fmt.Fprintf(os.Stderr, "mcpb-gen: %v\n", err)
		os.Exit(1)
	}
}
