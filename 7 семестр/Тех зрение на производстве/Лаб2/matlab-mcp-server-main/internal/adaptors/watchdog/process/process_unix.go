// Copyright 2025 The MathWorks, Inc.
//go:build !windows

package process

import "syscall"

func getSysProcAttrForDetachingAProcess() *syscall.SysProcAttr {
	return &syscall.SysProcAttr{
		Setpgid: true,
		Pgid:    0,
	}
}
