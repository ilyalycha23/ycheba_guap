// Copyright 2026 The MathWorks, Inc.

package instruments_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/telemetry/otel/instruments"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/metric/noop"
)

func TestNewInt64Counter_HappyPath(t *testing.T) {
	// Arrange
	meter := noop.NewMeterProvider().Meter("test")
	expectedName := "test.counter"
	expectedDescription := "A test counter"
	expectedUnit := "{count}"

	// Act
	counter, err := instruments.NewInt64CounterForTesting(meter, expectedName, expectedDescription, expectedUnit)

	// Assert
	require.NoError(t, err)
	assert.NotNil(t, counter)
}

func TestInt64Counter_Add_HappyPath(t *testing.T) {
	// Arrange
	meter := noop.NewMeterProvider().Meter("test")
	counter, err := instruments.NewInt64CounterForTesting(meter, "test.counter", "A test counter", "{count}")
	require.NoError(t, err)

	expectedValue := int64(5)
	expectedAttrs := []attribute.KeyValue{
		attribute.String("key", "value"),
	}

	// Act & Assert (no panic)
	counter.Add(t.Context(), expectedValue, expectedAttrs)
}

func TestInt64Counter_Add_NilAttributes(t *testing.T) {
	// Arrange
	meter := noop.NewMeterProvider().Meter("test")
	counter, err := instruments.NewInt64CounterForTesting(meter, "test.counter", "A test counter", "{count}")
	require.NoError(t, err)

	expectedValue := int64(5)

	// Act & Assert (no panic when attrs is nil)
	counter.Add(t.Context(), expectedValue, nil)
}

func TestInt64Counter_Add_EmptyAttributes(t *testing.T) {
	// Arrange
	meter := noop.NewMeterProvider().Meter("test")
	counter, err := instruments.NewInt64CounterForTesting(meter, "test.counter", "A test counter", "{count}")
	require.NoError(t, err)

	expectedValue := int64(5)
	emptyAttrs := []attribute.KeyValue{}

	// Act & Assert (no panic when attrs is empty)
	counter.Add(t.Context(), expectedValue, emptyAttrs)
}
