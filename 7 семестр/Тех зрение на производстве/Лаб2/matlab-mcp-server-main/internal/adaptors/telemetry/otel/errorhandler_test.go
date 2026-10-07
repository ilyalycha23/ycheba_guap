// Copyright 2026 The MathWorks, Inc.

package otel_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/telemetry/otel"
	"github.com/matlab/matlab-mcp-server/internal/testutils"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestLoggerErrorHandler_Handle_HappyPath(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	handler := otel.NewLoggerErrorHandler(mockLogger)

	// Act
	handler.Handle(assert.AnError)

	// Assert
	logs := mockLogger.WarnLogs()
	require.Len(t, logs, 1)

	fields, found := logs["OpenTelemetry error"]
	require.True(t, found, "Expected a warning log with message 'OpenTelemetry error'")

	errField, found := fields["error"]
	require.True(t, found, "Expected an error field in the warning log")

	assert.Equal(t, assert.AnError, errField)
}
