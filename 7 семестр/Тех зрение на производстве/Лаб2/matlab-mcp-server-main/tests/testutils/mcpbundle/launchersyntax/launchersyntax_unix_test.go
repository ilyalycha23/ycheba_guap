// Copyright 2026 The MathWorks, Inc.

//go:build !windows

package launchersyntax_test

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/matlab/matlab-mcp-server/tests/testutils/mcpbundle/launchersyntax"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestCheck_ValidScript(t *testing.T) {
	path := filepath.Join(t.TempDir(), "script.sh")
	require.NoError(t, os.WriteFile(path, []byte("#!/bin/bash\necho hello\n"), 0o755)) //nolint:gosec // Test script needs execute permission

	assert.NoError(t, launchersyntax.Check(path))
}

func TestCheck_InvalidScript(t *testing.T) {
	path := filepath.Join(t.TempDir(), "script.sh")
	require.NoError(t, os.WriteFile(path, []byte("#!/bin/bash\nif then fi\n"), 0o755)) //nolint:gosec // Test script needs execute permission

	assert.Error(t, launchersyntax.Check(path))
}

func TestCheck_MissingFile(t *testing.T) {
	path := filepath.Join(t.TempDir(), "nonexistent.sh")

	assert.Error(t, launchersyntax.Check(path))
}
