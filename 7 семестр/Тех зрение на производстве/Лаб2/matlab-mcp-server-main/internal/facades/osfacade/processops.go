// Copyright 2025 The MathWorks, Inc.

package osfacade

import (
	"os"
	"runtime/debug"
)

type Process interface {
	Signal(sig os.Signal) error
	Kill() error
	Wait() (*os.ProcessState, error)
}

// Command wraps the exec.Command
func (osw *OsFacade) FindProcess(pid int) (Process, error) {
	return os.FindProcess(pid)
}

// ReadBuildInfo wraps the debug.ReadBuildInfo
func (osw *OsFacade) ReadBuildInfo() (info *debug.BuildInfo, ok bool) {
	return debug.ReadBuildInfo()
}

// Executable wraps os.Executable
func (osw *OsFacade) Executable() (string, error) {
	return os.Executable()
}
