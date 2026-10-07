// Copyright 2026 The MathWorks, Inc.

//go:build windows

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
	path := filepath.Join(t.TempDir(), "script.cmd")
	require.NoError(t, os.WriteFile(path, []byte("@echo off\r\necho hello\r\n"), 0o600))

	assert.NoError(t, launchersyntax.Check(path))
}

func TestCheck_EmptyFile(t *testing.T) {
	path := filepath.Join(t.TempDir(), "script.cmd")
	require.NoError(t, os.WriteFile(path, []byte{}, 0o600))

	assert.Error(t, launchersyntax.Check(path))
}

func TestCheck_MissingFile(t *testing.T) {
	path := filepath.Join(t.TempDir(), "nonexistent.cmd")

	assert.Error(t, launchersyntax.Check(path))
}
