// Copyright 2026 The MathWorks, Inc.

package launcherflags_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/tests/testutils/mcpbundle/launcherflags"
	"github.com/stretchr/testify/assert"
)

func TestParse_ExtractsFlags(t *testing.T) {
	script := `#!/usr/bin/env bash
MCPB_MAPPINGS=(
    "__MATLAB_MCP_SERVER_MCPB_MATLAB_ROOT:string:--matlab-root"
    "__MATLAB_MCP_SERVER_MCPB_INIT_ON_START:bool:--initialize-matlab-on-startup"
    "__MATLAB_MCP_SERVER_MCPB_DISPLAY_MODE:string:--matlab-display-mode"
)
`
	flags := launcherflags.Parse(script)

	assert.Equal(t, []string{
		"initialize-matlab-on-startup",
		"matlab-display-mode",
		"matlab-root",
	}, flags)
}

func TestParse_SortsAlphabetically(t *testing.T) {
	script := `
    "__MATLAB_MCP_SERVER_MCPB_C:string:--zebra"
    "__MATLAB_MCP_SERVER_MCPB_A:bool:--alpha"
    "__MATLAB_MCP_SERVER_MCPB_B:string:--middle"
`
	flags := launcherflags.Parse(script)

	assert.Equal(t, []string{"alpha", "middle", "zebra"}, flags)
}

func TestParse_DeduplicatesFlags(t *testing.T) {
	script := `
    "__MATLAB_MCP_SERVER_MCPB_FOO:string:--some-flag"
    "__MATLAB_MCP_SERVER_MCPB_BAR:bool:--some-flag"
`
	flags := launcherflags.Parse(script)

	assert.Equal(t, []string{"some-flag"}, flags)
}

func TestParse_IgnoresInvalidFormats(t *testing.T) {
	script := `
    "__MATLAB_MCP_SERVER_MCPB_VALID:string:--valid-flag"
    "INVALID_PREFIX:string:--not-captured"
    "__MATLAB_MCP_SERVER_MCPB_BAD:unknown:--bad-type"
`
	flags := launcherflags.Parse(script)

	assert.Equal(t, []string{"valid-flag"}, flags)
}

func TestParse_EmptyContent(t *testing.T) {
	assert.Empty(t, launcherflags.Parse(""))
}

func TestParse_NoMatches(t *testing.T) {
	assert.Empty(t, launcherflags.Parse("#!/bin/bash\necho hello"))
}
