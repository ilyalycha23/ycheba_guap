// Copyright 2025-2026 The MathWorks, Inc.

package mcpserver_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/tests/testutils/mcpserver"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestParseVersion_FullVersion(t *testing.T) {
	version, err := mcpserver.ParseVersion("github.com/matlab/matlab-mcp-server v1.2.3\n")

	require.NoError(t, err)
	assert.Equal(t, "v1.2.3", version)
}

func TestParseVersion_DevelVersion(t *testing.T) {
	version, err := mcpserver.ParseVersion("github.com/matlab/matlab-mcp-server (devel)\n")

	require.NoError(t, err)
	assert.Equal(t, "(devel)", version)
}

func TestParseVersion_EmptyOutput(t *testing.T) {
	_, err := mcpserver.ParseVersion("")

	require.Error(t, err)
	assert.Contains(t, err.Error(), "empty version output")
}

func TestParseVersion_WhitespaceOnly(t *testing.T) {
	_, err := mcpserver.ParseVersion("  \n  ")

	require.Error(t, err)
	assert.Contains(t, err.Error(), "empty version output")
}

func TestParseHelpFlags_ExtractsVisibleFlags(t *testing.T) {
	helpOutput := `Usage:
      --disable-telemetry                Disable telemetry collection
      --extension-file                   Path to extension file
      --help                             Display this help message
      --matlab-root                      Path to MATLAB installation
      --version                          Display version information
`
	flags := mcpserver.ParseHelpFlags(helpOutput)

	assert.Equal(t, []string{
		"disable-telemetry",
		"extension-file",
		"help",
		"matlab-root",
		"version",
	}, flags)
}

func TestParseHelpFlags_IgnoresLinesBeforeUsage(t *testing.T) {
	helpOutput := `Some preamble
      --not-a-flag     should be ignored
Usage:
      --real-flag      this one counts
`
	flags := mcpserver.ParseHelpFlags(helpOutput)

	assert.Equal(t, []string{"real-flag"}, flags)
}

func TestParseHelpFlags_EmptyOutput(t *testing.T) {
	assert.Empty(t, mcpserver.ParseHelpFlags(""))
}

func TestParseHelpFlags_NoUsageSection(t *testing.T) {
	assert.Empty(t, mcpserver.ParseHelpFlags("some random output\nwith no usage"))
}
