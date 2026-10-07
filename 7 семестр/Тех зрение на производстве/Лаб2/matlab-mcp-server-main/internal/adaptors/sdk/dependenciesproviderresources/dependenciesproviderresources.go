// Copyright 2026 The MathWorks, Inc.

package dependenciesproviderresources

import (
	"github.com/matlab/matlab-mcp-server/internal/adaptors/application/definition"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/config"
	publictypes "github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/watchdog"
	"github.com/matlab/matlab-mcp-server/internal/entities"
)

type LoggerFactory interface {
	New(logger entities.Logger) publictypes.Logger
}

type ConfigFactory interface {
	New(
		internalConfig config.InternalConfig,
		internalMessageCatalog config.InternalMessageCatalog,
	) publictypes.Config
}

type WatchdogFactory interface {
	New(
		logger entities.Logger,
		internalWatchdog watchdog.InternalWatchdog,
	) publictypes.Watchdog
}

type Factory struct {
	loggerFactory   LoggerFactory
	configFactory   ConfigFactory
	watchdogFactory WatchdogFactory
}

func NewFactory(
	loggerFactory LoggerFactory,
	configFactory ConfigFactory,
	watchdogFactory WatchdogFactory,
) *Factory {
	return &Factory{
		loggerFactory:   loggerFactory,
		configFactory:   configFactory,
		watchdogFactory: watchdogFactory,
	}
}

func (f *Factory) New(
	internal definition.DependenciesProviderResources,
) publictypes.DependenciesProviderResources {
	return &dependenciesProviderResourcesAdaptor{
		logger:   f.loggerFactory.New(internal.Logger),
		config:   f.configFactory.New(internal.Config, internal.MessageCatalog),
		watchdog: f.watchdogFactory.New(internal.Logger, internal.Watchdog),
	}
}

type dependenciesProviderResourcesAdaptor struct {
	logger   publictypes.Logger
	config   publictypes.Config
	watchdog publictypes.Watchdog
}

func (r *dependenciesProviderResourcesAdaptor) Logger() publictypes.Logger {
	return r.logger
}

func (r *dependenciesProviderResourcesAdaptor) Config() publictypes.Config {
	return r.config
}

func (r *dependenciesProviderResourcesAdaptor) Watchdog() publictypes.Watchdog {
	return r.watchdog
}
