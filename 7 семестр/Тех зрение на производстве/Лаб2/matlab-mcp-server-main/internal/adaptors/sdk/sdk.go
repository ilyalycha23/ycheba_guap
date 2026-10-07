// Copyright 2026 The MathWorks, Inc.

package sdk

import (
	"os"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/config"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/dependenciesprovider"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/dependenciesproviderresources"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/features"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/logger"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/messages"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/parameters"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/server"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/toolcallrequest"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/toolsprovider"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/toolsproviderresources"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/watchdog"
	"github.com/matlab/matlab-mcp-server/internal/wire/adaptor"
)

func NewServer[Dependencies any](
	serverDefinition server.Definition[Dependencies],
) *server.Server[Dependencies] {
	messagesFactory := messages.NewFactory()
	loggerFactory := logger.NewFactory()
	configFactory := config.NewFactory(messagesFactory)
	watchdogFactory := watchdog.NewFactory()
	dependenciesProviderResourcesFactory := dependenciesproviderresources.NewFactory(
		loggerFactory,
		configFactory,
		watchdogFactory,
	)
	dependenciesProviderFactory := dependenciesprovider.NewFactory[Dependencies](
		dependenciesProviderResourcesFactory,
	)
	toolsProviderResourcesFactory := toolsproviderresources.NewFactory[Dependencies](
		loggerFactory,
	)
	toolCallRequestFactory := toolcallrequest.NewFactory(
		loggerFactory,
		configFactory,
	)
	toolsProviderFactory := toolsprovider.NewFactory(
		toolsProviderResourcesFactory,
		toolCallRequestFactory,
	)
	parametersFactory := parameters.NewFactory()
	featuresFactory := features.NewFactory()
	applicationFactory := adaptor.NewFactory()

	return server.New(
		serverDefinition,
		featuresFactory,
		parametersFactory,
		dependenciesProviderFactory,
		toolsProviderFactory,
		applicationFactory,
		os.Stderr,
	)
}
