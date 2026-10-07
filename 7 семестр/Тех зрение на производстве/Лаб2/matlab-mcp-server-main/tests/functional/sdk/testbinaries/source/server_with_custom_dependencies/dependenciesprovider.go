// Copyright 2026 The MathWorks, Inc.

package main

import (
	"github.com/matlab/matlab-mcp-server/pkg/i18n"
	"github.com/matlab/matlab-mcp-server/pkg/logger"
)

type Dependencies struct {
	DataService *DataService
}

type DependenciesProviderResources interface {
	Logger() logger.Logger
}

func DependenciesProvider(resources DependenciesProviderResources) (Dependencies, i18n.Error) {
	resources.Logger().Info("Creating Dependencies")

	return Dependencies{
		DataService: NewDataService("Service Hello"),
	}, nil
}
