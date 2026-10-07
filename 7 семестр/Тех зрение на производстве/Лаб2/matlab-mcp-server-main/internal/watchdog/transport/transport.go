// Copyright 2025-2026 The MathWorks, Inc.

package transport

import "github.com/matlab/matlab-mcp-server/internal/watchdog/transport/messages"

type Client interface {
	Connect(socketPath string) error
	SendProcessPID(pid int) (messages.ProcessToKillResponse, error)
	SendStop() (messages.ShutdownResponse, error)
	Close() error
}

type Server interface {
	Start(socketPath string) error
	Stop() error
}
