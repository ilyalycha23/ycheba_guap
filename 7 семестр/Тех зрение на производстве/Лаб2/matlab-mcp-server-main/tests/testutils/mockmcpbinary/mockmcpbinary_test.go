// Copyright 2026 The MathWorks, Inc.

package mockmcpbinary_test

import (
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/matlab/matlab-mcp-server/tests/testutils/mockmcpbinary"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestLastInvocation_Success(t *testing.T) {
	outputFile := filepath.Join(t.TempDir(), "invocations.jsonl")
	writeJSONL(t, outputFile, []mockmcpbinary.Invocation{
		{Args: []string{"--version"}, Env: nil},
		{Args: []string{"--matlab-root", "/opt/matlab"}, Env: []string{"__MATLAB_MCP_SERVER_MCPB_FOO=bar"}},
	})

	installation := &mockmcpbinary.Installation{
		BinaryPath: "/fake/binary",
		OutputFile: outputFile,
	}

	inv, err := installation.LastInvocation()

	require.NoError(t, err)
	assert.Equal(t, []string{"--matlab-root", "/opt/matlab"}, inv.Args)
	assert.Equal(t, []string{"__MATLAB_MCP_SERVER_MCPB_FOO=bar"}, inv.Env)
}

func TestLastInvocation_MissingFile(t *testing.T) {
	installation := &mockmcpbinary.Installation{
		BinaryPath: "/fake/binary",
		OutputFile: filepath.Join(t.TempDir(), "nonexistent.jsonl"),
	}

	_, err := installation.LastInvocation()

	require.Error(t, err)
	assert.Contains(t, err.Error(), "reading invocation file")
}

func TestLastInvocation_EmptyFile(t *testing.T) {
	outputFile := filepath.Join(t.TempDir(), "invocations.jsonl")
	require.NoError(t, os.WriteFile(outputFile, []byte(""), 0o600))

	installation := &mockmcpbinary.Installation{
		BinaryPath: "/fake/binary",
		OutputFile: outputFile,
	}

	_, err := installation.LastInvocation()

	require.Error(t, err)
	assert.Contains(t, err.Error(), "no invocations recorded")
}

func TestLastInvocation_InvalidJSON(t *testing.T) {
	outputFile := filepath.Join(t.TempDir(), "invocations.jsonl")
	require.NoError(t, os.WriteFile(outputFile, []byte("not json\n"), 0o600))

	installation := &mockmcpbinary.Installation{
		BinaryPath: "/fake/binary",
		OutputFile: outputFile,
	}

	_, err := installation.LastInvocation()

	require.Error(t, err)
	assert.Contains(t, err.Error(), "parsing invocation line")
}

func TestInvocations_MultipleEntries(t *testing.T) {
	outputFile := filepath.Join(t.TempDir(), "invocations.jsonl")
	writeJSONL(t, outputFile, []mockmcpbinary.Invocation{
		{Args: []string{"--version"}, Env: nil},
		{Args: []string{"--help"}, Env: nil},
		{Args: []string{"--matlab-root", "/opt"}, Env: []string{"FOO=bar"}},
	})

	installation := &mockmcpbinary.Installation{
		BinaryPath: "/fake/binary",
		OutputFile: outputFile,
	}

	invocations, err := installation.Invocations()

	require.NoError(t, err)
	assert.Len(t, invocations, 3)
	assert.Equal(t, []string{"--version"}, invocations[0].Args)
	assert.Equal(t, []string{"--help"}, invocations[1].Args)
	assert.Equal(t, []string{"--matlab-root", "/opt"}, invocations[2].Args)
}

func TestInvocationCount_ReturnsCount(t *testing.T) {
	outputFile := filepath.Join(t.TempDir(), "invocations.jsonl")
	writeJSONL(t, outputFile, []mockmcpbinary.Invocation{
		{Args: []string{"--version"}},
		{Args: []string{"--help"}},
	})

	installation := &mockmcpbinary.Installation{
		BinaryPath: "/fake/binary",
		OutputFile: outputFile,
	}

	count, err := installation.InvocationCount()

	require.NoError(t, err)
	assert.Equal(t, 2, count)
}

func TestInvocationCount_ZeroWhenEmpty(t *testing.T) {
	outputFile := filepath.Join(t.TempDir(), "invocations.jsonl")
	require.NoError(t, os.WriteFile(outputFile, []byte(""), 0o600))

	installation := &mockmcpbinary.Installation{
		BinaryPath: "/fake/binary",
		OutputFile: outputFile,
	}

	count, err := installation.InvocationCount()

	require.NoError(t, err)
	assert.Equal(t, 0, count)
}

func TestReset_TruncatesFile(t *testing.T) {
	outputFile := filepath.Join(t.TempDir(), "invocations.jsonl")
	writeJSONL(t, outputFile, []mockmcpbinary.Invocation{
		{Args: []string{"--version"}},
	})

	installation := &mockmcpbinary.Installation{
		BinaryPath: "/fake/binary",
		OutputFile: outputFile,
	}

	require.NoError(t, installation.Reset())

	count, err := installation.InvocationCount()
	require.NoError(t, err)
	assert.Equal(t, 0, count)
}

func writeJSONL(t *testing.T, path string, invocations []mockmcpbinary.Invocation) {
	t.Helper()
	var lines []string
	for _, inv := range invocations {
		data, err := json.Marshal(inv)
		require.NoError(t, err)
		lines = append(lines, string(data))
	}
	content := strings.Join(lines, "\n") + "\n"
	require.NoError(t, os.WriteFile(path, []byte(content), 0o600))
}
