// Copyright 2026 The MathWorks, Inc.

package otel

import (
	"github.com/matlab/matlab-mcp-server/internal/entities"
	"go.opentelemetry.io/otel"
)

func SetErrorHandler(logger entities.Logger) {
	handler := newLoggerErrorHandler(logger)
	otel.SetErrorHandler(handler)
}

type loggerErrorHandler struct {
	logger entities.Logger
}

func newLoggerErrorHandler(logger entities.Logger) *loggerErrorHandler {
	return &loggerErrorHandler{
		logger: logger,
	}
}

func (h *loggerErrorHandler) Handle(err error) {
	h.logger.
		WithError(err).
		Warn("OpenTelemetry error")
}
