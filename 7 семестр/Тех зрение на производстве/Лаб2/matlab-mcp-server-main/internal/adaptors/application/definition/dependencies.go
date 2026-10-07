// Copyright 2026 The MathWorks, Inc.

package definition

import (
	"github.com/matlab/matlab-mcp-server/internal/adaptors/application/config"
	"github.com/matlab/matlab-mcp-server/internal/entities"
)

type Watchdog interface {
	RegisterProcessPIDWithWatchdog(processPID int) error
}

type DependenciesProviderResources struct {
	Logger         entities.Logger
	Config         config.GenericConfig
	MessageCatalog MessageCatalog
	Watchdog       Watchdog
}

type DependenciesProvider func(resources DependenciesProviderResources) (any, error)

func NewDependenciesProviderResources(
	logger entities.Logger,
	config config.GenericConfig,
	messageCatalog MessageCatalog,
	watchdog Watchdog,
) DependenciesProviderResources {
	return DependenciesProviderResources{
		Logger:         logger,
		Config:         config,
		MessageCatalog: messageCatalog,
		Watchdog:       watchdog,
	}
}
