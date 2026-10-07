// Copyright 2026 The MathWorks, Inc.

package logger

import (
	publictypes "github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
	"github.com/matlab/matlab-mcp-server/internal/entities"
)

type Factory struct{}

func NewFactory() *Factory {
	return &Factory{}
}

func (f *Factory) New(logger entities.Logger) publictypes.Logger {
	return &loggerAdaptor{
		Logger: logger,
	}
}

type loggerAdaptor struct {
	entities.Logger
}

func (l *loggerAdaptor) With(key string, value any) publictypes.Logger {
	newLogger := l.Logger.With(key, value)
	return &loggerAdaptor{
		Logger: newLogger,
	}
}

func (l *loggerAdaptor) WithError(err error) publictypes.Logger {
	newLogger := l.Logger.WithError(err)
	return &loggerAdaptor{
		Logger: newLogger,
	}
}
