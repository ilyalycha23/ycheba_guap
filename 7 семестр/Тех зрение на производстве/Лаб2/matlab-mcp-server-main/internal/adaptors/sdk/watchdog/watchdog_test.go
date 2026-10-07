// Copyright 2026 The MathWorks, Inc.

package watchdog_test

import (
	"errors"
	"testing"

	watchdogadaptor "github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/watchdog"
	"github.com/matlab/matlab-mcp-server/internal/testutils"
	watchdogmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/sdk/watchdog"
	"github.com/stretchr/testify/require"
)

func TestNewFactory_HappyPath(t *testing.T) {
	// Arrange

	// Act
	factory := watchdogadaptor.NewFactory()

	// Assert
	require.NotNil(t, factory)
}

func TestFactory_New_HappyPath(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockInternalWatchdog := &watchdogmocks.MockInternalWatchdog{}
	defer mockInternalWatchdog.AssertExpectations(t)

	// Act
	adaptor := watchdogadaptor.NewFactory().New(mockLogger, mockInternalWatchdog)

	// Assert
	require.NotNil(t, adaptor)
}

func TestWatchdogAdaptor_WatchProcess_HappyPath(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockInternalWatchdog := &watchdogmocks.MockInternalWatchdog{}
	defer mockInternalWatchdog.AssertExpectations(t)

	expectedPID := 12345

	mockInternalWatchdog.EXPECT().
		RegisterProcessPIDWithWatchdog(expectedPID).
		Return(nil).
		Once()

	adaptor := watchdogadaptor.NewFactory().New(mockLogger, mockInternalWatchdog)

	// Act
	adaptor.WatchProcess(expectedPID)

	// Assert
	// Assertions are verified via deferred mock expectations.
}

func TestWatchdogAdaptor_WatchProcess_Error(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockInternalWatchdog := &watchdogmocks.MockInternalWatchdog{}
	defer mockInternalWatchdog.AssertExpectations(t)

	expectedPID := 12345
	expectedError := errors.New("watchdog registration failed")

	mockInternalWatchdog.EXPECT().
		RegisterProcessPIDWithWatchdog(expectedPID).
		Return(expectedError).
		Once()

	adaptor := watchdogadaptor.NewFactory().New(mockLogger, mockInternalWatchdog)

	// Act
	adaptor.WatchProcess(expectedPID)

	// Assert
	expectedMessage := "Failed to register process with watchdog"
	require.Contains(t, mockLogger.WarnLogs(), expectedMessage)
	require.Equal(t, expectedError, mockLogger.WarnLogs()[expectedMessage]["error"])
}
