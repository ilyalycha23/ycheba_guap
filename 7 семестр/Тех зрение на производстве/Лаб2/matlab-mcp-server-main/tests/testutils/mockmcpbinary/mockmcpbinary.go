// Copyright 2026 The MathWorks, Inc.

package mockmcpbinary

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/matlab/matlab-mcp-server/tests/testutils/mockmcpbinary/installer"
	"github.com/stretchr/testify/require"
)

const OutputFileEnvVar = "MOCK_MCPBINARY_OUTPUT_FILE"

type Invocation struct {
	Args []string `json:"args"`
	Env  []string `json:"env"`
}

type Installation struct {
	BinaryPath string
	OutputFile string
}

func (i *Installation) Invocations() ([]Invocation, error) {
	data, err := os.ReadFile(i.OutputFile)
	if err != nil {
		return nil, fmt.Errorf("reading invocation file: %w", err)
	}

	var invocations []Invocation
	scanner := bufio.NewScanner(strings.NewReader(string(data)))
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}
		var inv Invocation
		if err := json.Unmarshal([]byte(line), &inv); err != nil {
			return nil, fmt.Errorf("parsing invocation line: %w", err)
		}
		invocations = append(invocations, inv)
	}
	if err := scanner.Err(); err != nil {
		return nil, fmt.Errorf("scanning invocation file: %w", err)
	}
	return invocations, nil
}

func (i *Installation) LastInvocation() (Invocation, error) {
	invocations, err := i.Invocations()
	if err != nil {
		return Invocation{}, err
	}
	if len(invocations) == 0 {
		return Invocation{}, fmt.Errorf("no invocations recorded")
	}
	return invocations[len(invocations)-1], nil
}

func (i *Installation) InvocationCount() (int, error) {
	invocations, err := i.Invocations()
	if err != nil {
		return 0, err
	}
	return len(invocations), nil
}

func (i *Installation) Reset() error {
	return os.WriteFile(i.OutputFile, nil, 0o600)
}

func BuildAndInstall(t *testing.T, binDir string) *Installation {
	t.Helper()

	inst := installer.New(installer.GoListModuleRootFinder{}, installer.GoBinaryBuilder{})
	binaryPath, err := inst.BuildAndInstall(binDir)
	require.NoError(t, err, "building mock MCP binary")

	outputFile := filepath.Join(t.TempDir(), "invocations.jsonl")

	return &Installation{
		BinaryPath: binaryPath,
		OutputFile: outputFile,
	}
}
