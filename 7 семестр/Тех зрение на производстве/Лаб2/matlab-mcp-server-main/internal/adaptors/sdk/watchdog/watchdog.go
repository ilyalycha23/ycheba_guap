// Copyright 2026 The MathWorks, Inc.

package watchdog

import (
	publictypes "github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
	"github.com/matlab/matlab-mcp-server/internal/entities"
)

type InternalWatchdog interface {
	RegisterProcessPIDWithWatchdog(pid int) error
}

type Factory struct{}

func NewFactory() *Factory {
	return &Factory{}
}

func (f *Factory) New(
	logger entities.Logger,
	internalWatchdog InternalWatchdog,
) publictypes.Watchdog {
	return &watchdogAdaptor{
		logger:           logger,
		internalWatchdog: internalWatchdog,
	}
}

type watchdogAdaptor struct {
	logger           entities.Logger
	internalWatchdog InternalWatchdog
}

func (a *watchdogAdaptor) WatchProcess(pid int) {
	err := a.internalWatchdog.RegisterProcessPIDWithWatchdog(pid)
	if err != nil {
		a.logger.
			WithError(err).
			Warn("Failed to register process with watchdog")
	}
}
