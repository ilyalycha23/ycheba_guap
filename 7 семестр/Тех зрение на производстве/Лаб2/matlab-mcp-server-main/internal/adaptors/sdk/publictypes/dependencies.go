// Copyright 2026 The MathWorks, Inc.

package publictypes

type DependenciesProviderResources interface {
	Logger() Logger
	Config() Config
	Watchdog() Watchdog
}

type DependenciesProvider[Dependencies any] func(DependenciesProviderResources) (Dependencies, Error)
