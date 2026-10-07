// Copyright 2026 The MathWorks, Inc.

package instruments_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/telemetry/otel/instruments"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"go.opentelemetry.io/otel/metric/noop"
)

func TestNewFactory_HappyPath(t *testing.T) {
	// Act
	factory := instruments.NewFactory()

	// Assert
	assert.NotNil(t, factory)
}

func TestFactory_NewInt64Counter_HappyPath(t *testing.T) {
	// Arrange
	factory := instruments.NewFactory()
	meter := noop.NewMeterProvider().Meter("test")
	expectedName := "test.counter"
	expectedDescription := "A test counter"
	expectedUnit := "{count}"

	// Act
	counter, err := factory.NewInt64Counter(meter, expectedName, expectedDescription, expectedUnit)

	// Assert
	require.NoError(t, err)
	assert.NotNil(t, counter)
}
