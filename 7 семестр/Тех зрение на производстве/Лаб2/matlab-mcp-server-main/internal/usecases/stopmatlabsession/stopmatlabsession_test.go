// Copyright 2025-2026 The MathWorks, Inc.

package stopmatlabsession_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/testutils"
	"github.com/matlab/matlab-mcp-server/internal/usecases/stopmatlabsession"
	entitiesmocks "github.com/matlab/matlab-mcp-server/mocks/entities"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestNew_HappyPath(t *testing.T) {
	// Arrange
	mockMATLABManager := &entitiesmocks.MockMATLABManager{}
	defer mockMATLABManager.AssertExpectations(t)

	// Act
	usecase := stopmatlabsession.New(mockMATLABManager)

	// Assert
	assert.NotNil(t, usecase, "Usecase should not be nil")
}

func TestUsecase_Execute_HappyPath(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockMATLABManager := &entitiesmocks.MockMATLABManager{}
	defer mockMATLABManager.AssertExpectations(t)

	ctx := t.Context()
	const sessionID = entities.SessionID(2)

	mockMATLABManager.EXPECT().
		StopMATLABSession(ctx, mockLogger.AsMockArg(), sessionID).
		Return(nil).
		Once()

	usecase := stopmatlabsession.New(mockMATLABManager)

	// Act
	err := usecase.Execute(ctx, mockLogger, sessionID)

	// Assert
	assert.NoError(t, err, "Execute should not return an error")
}

func TestUsecase_Execute_MATLABManagerReturnsError(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockMATLABManager := &entitiesmocks.MockMATLABManager{}
	defer mockMATLABManager.AssertExpectations(t)

	ctx := t.Context()
	const sessionID = entities.SessionID(2)
	expectedError := assert.AnError

	mockMATLABManager.EXPECT().
		StopMATLABSession(ctx, mockLogger.AsMockArg(), sessionID).
		Return(expectedError).
		Once()

	usecase := stopmatlabsession.New(mockMATLABManager)

	// Act
	err := usecase.Execute(ctx, mockLogger, sessionID)

	// Assert
	require.Error(t, err, "Execute should return an error")
	assert.ErrorIs(t, err, expectedError, "Error should be the original error")
}
