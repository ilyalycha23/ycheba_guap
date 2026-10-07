// Copyright 2026 The MathWorks, Inc.

package main

import (
	"github.com/matlab/matlab-mcp-server/pkg/i18n"
	"github.com/matlab/matlab-mcp-server/pkg/watchdog"
)

type Dependencies struct {
	ExternalService *ExternalService
}

type DependenciesProviderResources interface {
	Watchdog() watchdog.Watchdog
}

func DependenciesProvider(resources DependenciesProviderResources) (Dependencies, i18n.Error) {
	service := NewExternalService()

	pid, err := service.Start()
	if err != nil {
		return Dependencies{}, ServiceStartErr
	}

	resources.Watchdog().WatchProcess(pid)

	return Dependencies{
		ExternalService: service,
	}, nil
}
