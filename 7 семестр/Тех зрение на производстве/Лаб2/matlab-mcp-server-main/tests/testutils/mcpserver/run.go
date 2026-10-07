// Copyright 2025-2026 The MathWorks, Inc.

package mcpserver

import (
	"fmt"
	"os"
	"os/exec"
	"testing"

	"github.com/stretchr/testify/require"
)

func Run(t *testing.T, binaryPath string, flags []string, env map[string]string) string {
	t.Helper()
	cmd := exec.CommandContext(t.Context(), binaryPath, flags...)
	if len(env) > 0 {
		cmd.Env = os.Environ()
		for k, v := range env {
			cmd.Env = append(cmd.Env, fmt.Sprintf("%s=%s", k, v))
		}
	}
	output, err := cmd.CombinedOutput()
	require.NoError(t, err, "%v failed: %s", flags, output)
	return string(output)
}
