// Copyright 2025-2026 The MathWorks, Inc.

package startmatlabsession_test

import (
	"path/filepath"
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/testutils"
	"github.com/matlab/matlab-mcp-server/internal/usecases/startmatlabsession"
	entitiesmocks "github.com/matlab/matlab-mcp-server/mocks/entities"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

const (
	verCode    = "ver"
	addOnsCode = "matlab.addons.installedAddons()"
)

func TestNew_HappyPath(t *testing.T) {
	// Arrange
	mockMATLABManager := &entitiesmocks.MockMATLABManager{}
	defer mockMATLABManager.AssertExpectations(t)

	// Act
	usecase := startmatlabsession.New(mockMATLABManager)

	// Assert
	assert.NotNil(t, usecase, "Usecase should not be nil")
}

func TestUsecase_Execute_HappyPath(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockMATLABManager := &entitiesmocks.MockMATLABManager{}
	defer mockMATLABManager.AssertExpectations(t)

	mockClient := &entitiesmocks.MockMATLABSessionClient{}
	defer mockClient.AssertExpectations(t)

	startSessionRequest := entities.LocalSessionDetails{
		MATLABRoot: filepath.Join("path", "to", "matlab", "R2023a"),
	}

	ctx := t.Context()
	const expectedSessionID = entities.SessionID(123)
	const expectedVerOutput = "MATLAB Version: X (R2024b)"
	const expectedAddOnsOutput = "GUI Layout Toolbox"

	mockMATLABManager.EXPECT().
		StartMATLABSession(ctx, mockLogger.AsMockArg(), startSessionRequest).
		Return(expectedSessionID, nil).
		Once()

	mockMATLABManager.EXPECT().
		GetMATLABSessionClient(ctx, mockLogger.AsMockArg(), expectedSessionID).
		Return(mockClient, nil).
		Once()

	// Mock the EvalInMATLABSession calls
	mockClient.EXPECT().
		Eval(ctx, mockLogger.AsMockArg(), entities.EvalRequest{Code: verCode}).
		Return(entities.EvalResponse{ConsoleOutput: expectedVerOutput}, nil).
		Once()

	mockClient.EXPECT().
		Eval(ctx, mockLogger.AsMockArg(), entities.EvalRequest{Code: addOnsCode}).
		Return(entities.EvalResponse{ConsoleOutput: expectedAddOnsOutput}, nil).
		Once()

	usecase := startmatlabsession.New(mockMATLABManager)

	// Act
	response, err := usecase.Execute(ctx, mockLogger, startSessionRequest)

	// Assert
	require.NoError(t, err, "Execute should not return an error")
	assert.Equal(t, expectedSessionID, response.SessionID, "Session ID should match expected value")
	assert.Equal(t, expectedVerOutput, response.VerOutput, "Ver output should match expected value")
	assert.Equal(t, expectedAddOnsOutput, response.AddOnsOutput, "AddOns output should match expected value")
}

func TestUsecase_Execute_StartSessionError(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockMATLABManager := &entitiesmocks.MockMATLABManager{}
	defer mockMATLABManager.AssertExpectations(t)

	startSessionRequest := entities.LocalSessionDetails{
		MATLABRoot: filepath.Join("path", "to", "matlab", "R2023a"),
	}

	ctx := t.Context()
	const sessionIDThatShouldBeUnused = entities.SessionID(0)
	expectedError := assert.AnError

	mockMATLABManager.EXPECT().
		StartMATLABSession(ctx, mockLogger.AsMockArg(), startSessionRequest).
		Return(sessionIDThatShouldBeUnused, expectedError).
		Once()

	usecase := startmatlabsession.New(mockMATLABManager)

	// Act
	response, err := usecase.Execute(ctx, mockLogger, startSessionRequest)

	// Assert
	require.Error(t, err, "Execute should return an error")
	assert.Empty(t, response, "Response should be empty when there's an error")
	assert.ErrorIs(t, err, expectedError, "Error should be the original error")
}

func TestUsecase_Execute_GetMATLABSessionClientError(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockMATLABManager := &entitiesmocks.MockMATLABManager{}
	defer mockMATLABManager.AssertExpectations(t)

	startSessionRequest := entities.LocalSessionDetails{
		MATLABRoot: filepath.Join("path", "to", "matlab", "R2023a"),
	}

	ctx := t.Context()
	const expectedSessionID = entities.SessionID(123)
	expectedError := assert.AnError

	mockMATLABManager.EXPECT().
		StartMATLABSession(ctx, mockLogger.AsMockArg(), startSessionRequest).
		Return(expectedSessionID, nil).
		Once()

	mockMATLABManager.EXPECT().
		GetMATLABSessionClient(ctx, mockLogger.AsMockArg(), expectedSessionID).
		Return(nil, expectedError).
		Once()

	usecase := startmatlabsession.New(mockMATLABManager)

	// Act
	response, err := usecase.Execute(ctx, mockLogger, startSessionRequest)

	// Assert
	require.Error(t, err, "Execute should return an error")
	assert.Empty(t, response, "Response should be empty when there's an error")
	assert.ErrorIs(t, err, expectedError, "Error should be the original error")
}

func TestUsecase_Execute_VerEvalError(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockMATLABManager := &entitiesmocks.MockMATLABManager{}
	defer mockMATLABManager.AssertExpectations(t)

	mockClient := &entitiesmocks.MockMATLABSessionClient{}
	defer mockClient.AssertExpectations(t)

	startSessionRequest := entities.LocalSessionDetails{
		MATLABRoot: filepath.Join("path", "to", "matlab", "R2023a"),
	}

	ctx := t.Context()
	const expectedSessionID = entities.SessionID(123)
	expectedError := assert.AnError

	mockMATLABManager.EXPECT().
		StartMATLABSession(ctx, mockLogger.AsMockArg(), startSessionRequest).
		Return(expectedSessionID, nil).
		Once()

	mockMATLABManager.EXPECT().
		GetMATLABSessionClient(ctx, mockLogger.AsMockArg(), expectedSessionID).
		Return(mockClient, nil).
		Once()

	mockClient.EXPECT().
		Eval(ctx, mockLogger.AsMockArg(), entities.EvalRequest{Code: verCode}).
		Return(entities.EvalResponse{}, expectedError).
		Once()

	usecase := startmatlabsession.New(mockMATLABManager)

	// Act
	response, err := usecase.Execute(ctx, mockLogger, startSessionRequest)

	// Assert
	require.Error(t, err, "Execute should return an error")
	assert.Empty(t, response, "Response should be empty when there's an error")
	assert.ErrorIs(t, err, expectedError, "Error should be the original error")
}

func TestUsecase_Execute_AddOnsEvalError(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockMATLABManager := &entitiesmocks.MockMATLABManager{}
	defer mockMATLABManager.AssertExpectations(t)

	mockClient := &entitiesmocks.MockMATLABSessionClient{}
	defer mockClient.AssertExpectations(t)

	startSessionRequest := entities.LocalSessionDetails{
		MATLABRoot: filepath.Join("path", "to", "matlab", "R2023a"),
	}

	ctx := t.Context()
	const expectedSessionID = entities.SessionID(123)
	const expectedVerOutput = "MATLAB Version: X (R2024b)"
	expectedError := assert.AnError

	mockMATLABManager.EXPECT().
		StartMATLABSession(ctx, mockLogger.AsMockArg(), startSessionRequest).
		Return(expectedSessionID, nil).
		Once()

	mockMATLABManager.EXPECT().
		GetMATLABSessionClient(ctx, mockLogger.AsMockArg(), expectedSessionID).
		Return(mockClient, nil).
		Once()

	mockClient.EXPECT().
		Eval(ctx, mockLogger.AsMockArg(), entities.EvalRequest{Code: verCode}).
		Return(entities.EvalResponse{ConsoleOutput: expectedVerOutput}, nil).
		Once()

	// Mock the second EvalInMATLABSession call to fail
	mockClient.EXPECT().
		Eval(ctx, mockLogger.AsMockArg(), entities.EvalRequest{Code: addOnsCode}).
		Return(entities.EvalResponse{}, expectedError).
		Once()

	usecase := startmatlabsession.New(mockMATLABManager)

	// Act
	response, err := usecase.Execute(ctx, mockLogger, startSessionRequest)

	// Assert
	require.Error(t, err, "Execute should return an error")
	assert.Empty(t, response, "Response should be empty when there's an error")
	assert.ErrorIs(t, err, expectedError, "Error should be the original error")
}
