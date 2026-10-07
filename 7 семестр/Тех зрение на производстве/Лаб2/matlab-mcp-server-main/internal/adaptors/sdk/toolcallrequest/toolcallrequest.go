// Copyright 2026 The MathWorks, Inc.

package toolcallrequest

import (
	internalconfig "github.com/matlab/matlab-mcp-server/internal/adaptors/application/config"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/application/definition"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/config"
	publictypes "github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
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

type Factory struct {
	loggerFactory LoggerFactory
	configFactory ConfigFactory
}

func NewFactory(
	loggerFactory LoggerFactory,
	configFactory ConfigFactory,
) *Factory {
	return &Factory{
		loggerFactory: loggerFactory,
		configFactory: configFactory,
	}
}

func (f *Factory) New(
	internalLogger entities.Logger,
	internalConfig internalconfig.GenericConfig,
	internalMessageCatalog definition.MessageCatalog,
) publictypes.ToolCallRequest {
	return &toolCallRequestAdaptor{
		logger: f.loggerFactory.New(internalLogger),
		config: f.configFactory.New(internalConfig, internalMessageCatalog),
	}
}

type toolCallRequestAdaptor struct {
	logger publictypes.Logger
	config publictypes.Config
}

func (a *toolCallRequestAdaptor) Logger() publictypes.Logger {
	return a.logger
}

func (a *toolCallRequestAdaptor) Config() publictypes.Config {
	return a.config
}
