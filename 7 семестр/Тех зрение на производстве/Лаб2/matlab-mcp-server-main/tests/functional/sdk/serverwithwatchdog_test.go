// Copyright 2026 The MathWorks, Inc.

package sdk_test

import (
	"os"
	"runtime"
	"syscall"
	"testing"
	"time"

	"github.com/matlab/matlab-mcp-server/tests/functional/sdk/testbinaries"
	"github.com/stretchr/testify/suite"
)

// ServerWithWatchdogTestSuite tests SDK watchdog functionalities.
type ServerWithWatchdogTestSuite struct {
	SDKTestSuite

	serverDetails testbinaries.ServerWithWatchdogDetails
}

// SetupSuite runs once before all tests in a suite
func (s *ServerWithWatchdogTestSuite) SetupSuite() {
	s.serverDetails = testbinaries.BuildServerWithWatchdog(s.T())
}

func TestServerWithWatchdogTestSuite(t *testing.T) {
	suite.Run(t, new(ServerWithWatchdogTestSuite))
}

func (s *ServerWithWatchdogTestSuite) TestSDK_Watchdog_WatchedProcessIsKilledWhenSessionCloses() {
	// Arrange
	session := s.CreateSession(s.serverDetails.BinaryLocation(), nil, nil)
	defer func() {
		s.Require().NoError(session.Close())
	}()

	// Get the PID of the child process spawned and watched during dependency initialization
	result, err := session.CallTool(s.T().Context(), s.serverDetails.GetPIDToolName(), map[string]any{})
	s.Require().NoError(err, "should call get-pid tool successfully")

	var output struct {
		PID int `json:"pid"`
	}
	s.Require().NoError(session.UnmarshalStructuredContent(result, &output), "should unmarshal structured content")
	s.Require().NotZero(output.PID, "should return a valid PID")

	// Verify the child process is alive
	s.Require().True(isProcessAlive(output.PID), "child process should be alive before session close")

	// Act — close the session, which should trigger the watchdog to kill the child
	s.Require().NoError(session.Close(), "closing session should not error")

	// Assert — the child process should eventually be killed
	s.Require().Eventually(func() bool {
		return !isProcessAlive(output.PID)
	}, 10*time.Second, 1*time.Second, "watched child process should be killed after session close")
}

func isProcessAlive(pid int) bool {
	process, err := os.FindProcess(pid)
	if err != nil {
		return false
	}
	defer func() {
		_ = process.Release()
	}()
	if runtime.GOOS == "windows" {
		// For Windows that's all we need to do
		return true
	}
	return process.Signal(syscall.Signal(0)) == nil
}
