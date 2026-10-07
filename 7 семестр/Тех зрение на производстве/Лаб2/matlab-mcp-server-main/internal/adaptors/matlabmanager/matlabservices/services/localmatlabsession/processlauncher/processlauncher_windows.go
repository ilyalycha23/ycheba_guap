// Copyright 2025-2026 The MathWorks, Inc.
//go:build windows

package processlauncher

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"syscall"
	"unsafe"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/matlabmanager/matlabservices/config"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/matlabmanager/matlabservices/services/localmatlabsession/processlauncher/utils/winenvironmentbuilder"
	"github.com/matlab/matlab-mcp-server/internal/entities"
	"golang.org/x/sys/windows"
)

func startMatlab(_ context.Context, logger entities.Logger, matlabRoot string, workingDir string, args []string, env []string, stdIO *stdIO) (*os.Process, error) {
	matlabPath := filepath.Join(matlabRoot, "bin", config.ArchFolder, config.ArchSpecificExeName)

	if _, err := os.Stat(matlabPath); err != nil {
		return nil, err
	}

	// Careful on Windows, we need to quote the args
	cmdLineParts := make([]string, len(args)+1)
	cmdLineParts[0] = syscall.EscapeArg(matlabPath)
	for i, arg := range args {
		cmdLineParts[i+1] = syscall.EscapeArg(arg)
	}
	cmdLine := strings.Join(cmdLineParts, " ")

	envBlock, err := winenvironmentbuilder.Build(env)
	if err != nil {
		return nil, fmt.Errorf("failed to build environment block: %w", err)
	}

	envPtr := envBlock.PointerToFirstElement()
	if envPtr == nil {
		return nil, fmt.Errorf("failed to get environment block pointer")
	}

	cmdLinePtr, err := windows.UTF16PtrFromString(cmdLine)
	if err != nil {
		return nil, fmt.Errorf("error converting command line: %w", err)
	}

	workingDirPtr, err := windows.UTF16PtrFromString(workingDir)
	if err != nil {
		return nil, fmt.Errorf("error converting working directory: %w", err)
	}

	var si windows.StartupInfo
	var pi windows.ProcessInformation

	si.Cb = uint32(unsafe.Sizeof(si))

	si.Flags = windows.STARTF_USESTDHANDLES
	si.StdInput = windows.Handle(stdIO.stdIn.Fd())
	si.StdOutput = windows.Handle(stdIO.stdOut.Fd())
	si.StdErr = windows.Handle(stdIO.stdErr.Fd())

	creationFlags := uint32(windows.CREATE_NEW_PROCESS_GROUP | windows.DETACHED_PROCESS | windows.CREATE_UNICODE_ENVIRONMENT)

	err = windows.CreateProcess(
		nil,           // appName
		cmdLinePtr,    // commandLine
		nil,           // procSecurity
		nil,           // threadSecurity
		true,          // inheritHandles
		creationFlags, // creationFlags
		envPtr,        // env
		workingDirPtr, // currentDir
		&si,           // startupInfo
		&pi,           // outProcInfo
	)

	if err != nil {
		return nil, fmt.Errorf("error creating MATLAB process: %w", err)
	}

	// Close handles as we don't need them after FindProcess
	if closeErr := windows.CloseHandle(pi.Thread); closeErr != nil {
		logger.WithError(closeErr).Warn("failed to close thread handle")
	}
	if closeErr := windows.CloseHandle(pi.Process); closeErr != nil {
		logger.WithError(closeErr).Warn("failed to close process handle")
	}

	matlabProcess, err := os.FindProcess(int(pi.ProcessId))
	if err != nil {
		return nil, fmt.Errorf("error finding MATLAB process: %w", err)
	}

	return matlabProcess, nil
}
