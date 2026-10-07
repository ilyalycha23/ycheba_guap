// Copyright 2026 The MathWorks, Inc.

package main

import (
	"os"
	"os/exec"
)

const childProcessEnvVar = "SERVER_WITH_WATCHDOG_CHILD_MODE"

type ExternalService struct {
	PID int
}

func NewExternalService() *ExternalService {
	return &ExternalService{}
}

// Start spawns a long-running child process by re-launching the current binary
// with a sentinel environment variable set. When the binary detects this
// variable in main(), it blocks indefinitely instead of starting the MCP
// server. This approach is cross-platform (works on Windows, Linux, and macOS)
// and avoids depending on OS-specific commands like "sleep".
func (s *ExternalService) Start() (int, error) {
	cmd := exec.Command(os.Args[0]) //nolint:gosec // We control the input, and this test only
	cmd.Env = append(os.Environ(), childProcessEnvVar+"=1")
	if err := cmd.Start(); err != nil {
		return 0, err
	}
	s.PID = cmd.Process.Pid
	return s.PID, nil
}

func (s *ExternalService) GetData() string {
	// Dummy implementation for demo purposes
	return ""
}
