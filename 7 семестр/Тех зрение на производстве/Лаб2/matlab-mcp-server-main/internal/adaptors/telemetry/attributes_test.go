// Copyright 2026 The MathWorks, Inc.

package telemetry_test

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"go.opentelemetry.io/otel/attribute"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/telemetry"
	"github.com/matlab/matlab-mcp-server/internal/testutils"
)

func TestNewAttributes_HappyPath(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	// Act
	attrs := telemetry.NewAttributes(testLogger)

	// Assert
	require.NotNil(t, attrs)
}

func TestAttributes_AddString_HappyPath(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	key := "test-key"
	value := "test-value"

	// Act
	attrs.AddString(key, value)

	// Assert
	otelAttrs := attrs.AsOTEL()
	require.Len(t, otelAttrs, 1)
	assert.Equal(t, attribute.String(key, value), otelAttrs[0])
}

func TestAttributes_AddString_EmptyKey(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	expectedLogMessage := "Failed to add  attribute"

	// Act
	attrs.AddString("", "value")

	// Assert
	otelAttrs := attrs.AsOTEL()
	assert.Empty(t, otelAttrs)
	debugLogs := testLogger.DebugLogs()
	assert.Len(t, debugLogs, 1)
	assert.Contains(t, debugLogs, expectedLogMessage)
}

func TestAttributes_AddString_DuplicateKey(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	key := "duplicate-key"
	expectedLogMessage := "Failed to add " + key + " attribute"
	attrs.AddString(key, "first-value")

	// Act
	attrs.AddString(key, "second-value")

	// Assert
	otelAttrs := attrs.AsOTEL()
	require.Len(t, otelAttrs, 1)
	assert.Equal(t, attribute.String(key, "first-value"), otelAttrs[0])
	debugLogs := testLogger.DebugLogs()
	assert.Len(t, debugLogs, 1)
	assert.Contains(t, debugLogs, expectedLogMessage)
}

func TestAttributes_AddInt64_HappyPath(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	key := "test-key"
	value := int64(42)

	// Act
	attrs.AddInt64(key, value)

	// Assert
	otelAttrs := attrs.AsOTEL()
	require.Len(t, otelAttrs, 1)
	assert.Equal(t, attribute.Int64(key, value), otelAttrs[0])
}

func TestAttributes_AddInt64_EmptyKey(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	expectedLogMessage := "Failed to add  attribute"

	// Act
	attrs.AddInt64("", 42)

	// Assert
	otelAttrs := attrs.AsOTEL()
	assert.Empty(t, otelAttrs)
	debugLogs := testLogger.DebugLogs()
	assert.Len(t, debugLogs, 1)
	assert.Contains(t, debugLogs, expectedLogMessage)
}

func TestAttributes_AddInt64_DuplicateKey(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	key := "duplicate-key"
	expectedLogMessage := "Failed to add " + key + " attribute"
	attrs.AddInt64(key, 42)

	// Act
	attrs.AddInt64(key, 100)

	// Assert
	otelAttrs := attrs.AsOTEL()
	require.Len(t, otelAttrs, 1)
	assert.Equal(t, attribute.Int64(key, int64(42)), otelAttrs[0])
	debugLogs := testLogger.DebugLogs()
	assert.Len(t, debugLogs, 1)
	assert.Contains(t, debugLogs, expectedLogMessage)
}

func TestAttributes_AddFloat64_HappyPath(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	key := "test-key"
	value := 3.14

	// Act
	attrs.AddFloat64(key, value)

	// Assert
	otelAttrs := attrs.AsOTEL()
	require.Len(t, otelAttrs, 1)
	assert.Equal(t, attribute.Float64(key, value), otelAttrs[0])
}

func TestAttributes_AddFloat64_EmptyKey(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	expectedLogMessage := "Failed to add  attribute"

	// Act
	attrs.AddFloat64("", 3.14)

	// Assert
	otelAttrs := attrs.AsOTEL()
	assert.Empty(t, otelAttrs)
	debugLogs := testLogger.DebugLogs()
	assert.Len(t, debugLogs, 1)
	assert.Contains(t, debugLogs, expectedLogMessage)
}

func TestAttributes_AddFloat64_DuplicateKey(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	key := "duplicate-key"
	expectedLogMessage := "Failed to add " + key + " attribute"
	attrs.AddFloat64(key, 3.14)

	// Act
	attrs.AddFloat64(key, 2.71)

	// Assert
	otelAttrs := attrs.AsOTEL()
	require.Len(t, otelAttrs, 1)
	assert.Equal(t, attribute.Float64(key, 3.14), otelAttrs[0])
	debugLogs := testLogger.DebugLogs()
	assert.Len(t, debugLogs, 1)
	assert.Contains(t, debugLogs, expectedLogMessage)
}

func TestAttributes_AddBool_HappyPath(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	key := "test-key"
	value := true

	// Act
	attrs.AddBool(key, value)

	// Assert
	otelAttrs := attrs.AsOTEL()
	require.Len(t, otelAttrs, 1)
	assert.Equal(t, attribute.Bool(key, value), otelAttrs[0])
}

func TestAttributes_AddBool_EmptyKey(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	expectedLogMessage := "Failed to add  attribute"

	// Act
	attrs.AddBool("", true)

	// Assert
	otelAttrs := attrs.AsOTEL()
	assert.Empty(t, otelAttrs)
	debugLogs := testLogger.DebugLogs()
	assert.Len(t, debugLogs, 1)
	assert.Contains(t, debugLogs, expectedLogMessage)
}

func TestAttributes_AddBool_DuplicateKey(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	key := "duplicate-key"
	expectedLogMessage := "Failed to add " + key + " attribute"
	attrs.AddBool(key, true)

	// Act
	attrs.AddBool(key, false)

	// Assert
	otelAttrs := attrs.AsOTEL()
	require.Len(t, otelAttrs, 1)
	assert.Equal(t, attribute.Bool(key, true), otelAttrs[0])
	debugLogs := testLogger.DebugLogs()
	assert.Len(t, debugLogs, 1)
	assert.Contains(t, debugLogs, expectedLogMessage)
}

func TestAttributes_AddStringSlice_HappyPath(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	key := "test-key"
	value := []string{"a", "b", "c"}

	// Act
	attrs.AddStringSlice(key, value)

	// Assert
	otelAttrs := attrs.AsOTEL()
	require.Len(t, otelAttrs, 1)
	assert.Equal(t, attribute.StringSlice(key, value), otelAttrs[0])
}

func TestAttributes_AddStringSlice_EmptyKey(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	expectedLogMessage := "Failed to add  attribute"

	// Act
	attrs.AddStringSlice("", []string{"a", "b"})

	// Assert
	otelAttrs := attrs.AsOTEL()
	assert.Empty(t, otelAttrs)
	debugLogs := testLogger.DebugLogs()
	assert.Len(t, debugLogs, 1)
	assert.Contains(t, debugLogs, expectedLogMessage)
}

func TestAttributes_AddStringSlice_DuplicateKey(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	key := "duplicate-key"
	expectedLogMessage := "Failed to add " + key + " attribute"
	attrs.AddStringSlice(key, []string{"a"})

	// Act
	attrs.AddStringSlice(key, []string{"b"})

	// Assert
	otelAttrs := attrs.AsOTEL()
	require.Len(t, otelAttrs, 1)
	assert.Equal(t, attribute.StringSlice(key, []string{"a"}), otelAttrs[0])
	debugLogs := testLogger.DebugLogs()
	assert.Len(t, debugLogs, 1)
	assert.Contains(t, debugLogs, expectedLogMessage)
}

func TestAttributes_AsOTEL_HappyPath(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	expectedKey := "string-key"
	expectedValue := "string-value"
	attrs.AddString(expectedKey, expectedValue)

	// Act
	otelAttrs := attrs.AsOTEL()

	// Assert
	require.Len(t, otelAttrs, 1)
	assert.Equal(t, attribute.String(expectedKey, expectedValue), otelAttrs[0])
}

func TestAttributes_AsOTEL_Empty(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)

	// Act
	otelAttrs := attrs.AsOTEL()

	// Assert
	require.NotNil(t, otelAttrs)
	assert.Empty(t, otelAttrs)
}

func TestAttributes_MultipleAttributes(t *testing.T) {
	// Arrange
	testLogger := testutils.NewInspectableLogger()

	attrs := telemetry.NewAttributes(testLogger)
	stringKey := "string-key"
	stringValue := "string-value"
	int64Key := "int64-key"
	int64Value := int64(42)
	float64Key := "float64-key"
	float64Value := 3.14
	boolKey := "bool-key"
	boolValue := true
	stringSliceKey := "string-slice-key"
	stringSliceValue := []string{"a", "b", "c"}

	// Act
	attrs.AddString(stringKey, stringValue)
	attrs.AddInt64(int64Key, int64Value)
	attrs.AddFloat64(float64Key, float64Value)
	attrs.AddBool(boolKey, boolValue)
	attrs.AddStringSlice(stringSliceKey, stringSliceValue)

	// Assert
	otelAttrs := attrs.AsOTEL()
	require.Len(t, otelAttrs, 5)
	assert.Equal(t, attribute.String(stringKey, stringValue), otelAttrs[0])
	assert.Equal(t, attribute.Int64(int64Key, int64Value), otelAttrs[1])
	assert.Equal(t, attribute.Float64(float64Key, float64Value), otelAttrs[2])
	assert.Equal(t, attribute.Bool(boolKey, boolValue), otelAttrs[3])
	assert.Equal(t, attribute.StringSlice(stringSliceKey, stringSliceValue), otelAttrs[4])
}
