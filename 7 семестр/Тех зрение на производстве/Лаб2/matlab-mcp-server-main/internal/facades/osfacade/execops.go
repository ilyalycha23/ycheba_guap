// Copyright 2025-2026 The MathWorks, Inc.

package osfacade

import (
	"io"
	"os"
	"os/exec"
	"syscall"
)

// Getppid wraps the os.Getppid function.
func (osw *OsFacade) Getppid() int {
	return os.Getppid()
}

// LookPath wraps the os/exec.LookPath function.
func (osw *OsFacade) LookPath(file string) (string, error) {
	return exec.LookPath(file)
}

type Cmd interface {
	StdinPipe() (io.Writer, error)
	StdoutPipe() (io.Reader, error)
	StderrPipe() (io.Reader, error)
	Start() error
	Output() ([]byte, error)
	SetSysProcAttr(attr *syscall.SysProcAttr)
}

// Command wraps the exec.Command
func (osw *OsFacade) Command(name string, arg ...string) Cmd {
	return &CmdWrapper{
		Cmd: exec.Command(name, arg...),
	}
}

type CmdWrapper struct {
	*exec.Cmd
}

func (c *CmdWrapper) StdinPipe() (io.Writer, error) {
	return c.Cmd.StdinPipe()
}

func (c *CmdWrapper) StdoutPipe() (io.Reader, error) {
	return c.Cmd.StdoutPipe()
}

func (c *CmdWrapper) StderrPipe() (io.Reader, error) {
	return c.Cmd.StderrPipe()
}

func (c *CmdWrapper) SetSysProcAttr(attr *syscall.SysProcAttr) {
	c.SysProcAttr = attr
}
