// Copyright 2025 The MathWorks, Inc.
//go:build windows

package process

import (
	"syscall"

	"golang.org/x/sys/windows"
)

func getSysProcAttrForDetachingAProcess() *syscall.SysProcAttr {
	return &syscall.SysProcAttr{
		CreationFlags: windows.CREATE_NEW_PROCESS_GROUP | windows.DETACHED_PROCESS,
	}
}
