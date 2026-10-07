// Copyright 2025-2026 The MathWorks, Inc.

package logger

import (
	"log/slog"

	"github.com/matlab/matlab-mcp-server/internal/entities"
)

type slogLogger struct {
	logger *slog.Logger
}

// Debug creates a debug-level log message.
func (sl *slogLogger) Debug(msg string) {
	sl.logger.Debug(msg)
}

// Info creates a info-level log message.
func (sl *slogLogger) Info(msg string) {
	sl.logger.Info(msg)
}

// Warn creates a warning-level log message.
func (sl *slogLogger) Warn(msg string) {
	sl.logger.Warn(msg)
}

// Error creates a error-level log message.
func (sl *slogLogger) Error(msg string) {
	sl.logger.Error(msg)
}

// With returns a new logger with an additional key-value pair in its logs.
func (sl *slogLogger) With(key string, value any) entities.Logger {
	return &slogLogger{
		logger: sl.logger.With(key, value),
	}
}

// WithError wraps the slogLogger.With function with a constant "error" key.
func (sl *slogLogger) WithError(value error) entities.Logger {
	const key = "error"
	return sl.With(key, value)
}
