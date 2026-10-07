// Copyright 2026 The MathWorks, Inc.

package matlabmanager_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/matlabmanager"
	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/testutils"
	mocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/matlabmanager"
	entitiesmocks "github.com/matlab/matlab-mcp-server/mocks/entities"
	"github.com/stretchr/testify/assert"
)

func TestRetrieveCorrelationID_HappyPath(t *testing.T) {
	// Arrange
	mockClient := &entitiesmocks.MockMATLABSessionClient{}
	defer mockClient.AssertExpectations(t)

	mockLogger := testutils.NewInspectableLogger()
	ctx := t.Context()

	expectedRequest := entities.EvalRequest{
		Code: matlabmanager.CorrelationIDRetrievalCode,
	}

	expectedCorrelationID := "session-abc-123"

	mockClient.EXPECT().
		Eval(ctx, mockLogger.AsMockArg(), expectedRequest).
		Return(entities.EvalResponse{ConsoleOutput: expectedCorrelationID + "\n"}, nil).
		Once()

	// Act
	result := matlabmanager.RetrieveCorrelationIDForTesting(ctx, mockLogger, mockClient)

	// Assert
	assert.Equal(t, expectedCorrelationID, result, "correlation ID trimmed of whitespace")
}

func TestRetrieveCorrelationID_EmptyResponse_ReturnsEmpty(t *testing.T) {
	// Arrange
	mockClient := &entitiesmocks.MockMATLABSessionClient{}
	defer mockClient.AssertExpectations(t)

	mockLogger := testutils.NewInspectableLogger()
	ctx := t.Context()

	expectedRequest := entities.EvalRequest{
		Code: matlabmanager.CorrelationIDRetrievalCode,
	}

	mockClient.EXPECT().
		Eval(ctx, mockLogger.AsMockArg(), expectedRequest).
		Return(entities.EvalResponse{ConsoleOutput: ""}, nil).
		Once()

	// Act
	result := matlabmanager.RetrieveCorrelationIDForTesting(ctx, mockLogger, mockClient)

	// Assert
	assert.Empty(t, result)
}

func TestRetrieveCorrelationID_EvalError_ReturnsEmpty(t *testing.T) {
	// Arrange
	mockClient := &entitiesmocks.MockMATLABSessionClient{}
	defer mockClient.AssertExpectations(t)

	mockLogger := testutils.NewInspectableLogger()
	ctx := t.Context()

	expectedRequest := entities.EvalRequest{
		Code: matlabmanager.CorrelationIDRetrievalCode,
	}

	evalErr := assert.AnError

	mockClient.EXPECT().
		Eval(ctx, mockLogger.AsMockArg(), expectedRequest).
		Return(entities.EvalResponse{}, evalErr).
		Once()

	// Act
	result := matlabmanager.RetrieveCorrelationIDForTesting(ctx, mockLogger, mockClient)

	// Assert
	assert.Empty(t, result, "eval error must not surface as a non-empty ID")
}

func TestMATLABManager_GetSessionCorrelationID_HappyPath(t *testing.T) {
	// Arrange
	mockMATLABServices := &mocks.MockMATLABServices{}
	defer mockMATLABServices.AssertExpectations(t)

	mockSessionStore := &mocks.MockMATLABSessionStore{}
	defer mockSessionStore.AssertExpectations(t)

	mockClientFactory := &mocks.MockMATLABSessionClientFactory{}
	defer mockClientFactory.AssertExpectations(t)

	mockSessionSelector := &mocks.MockSessionSelector{}
	defer mockSessionSelector.AssertExpectations(t)

	mockConfigFactory := &mocks.MockConfigFactory{}
	defer mockConfigFactory.AssertExpectations(t)

	mockClientInfoProvider := &mocks.MockMCPClientInfoProvider{}
	defer mockClientInfoProvider.AssertExpectations(t)

	mockConnectionIndicator := &mocks.MockConnectionIndicator{}
	defer mockConnectionIndicator.AssertExpectations(t)

	sessionID := entities.SessionID(7)
	expectedCorrelationID := "corr-42"

	mockSessionStore.EXPECT().
		CorrelationID(sessionID).
		Return(expectedCorrelationID).
		Once()

	manager := matlabmanager.New(mockConfigFactory, mockMATLABServices, mockSessionStore, mockClientFactory, mockSessionSelector, mockClientInfoProvider, mockConnectionIndicator)

	// Act
	result := manager.GetSessionCorrelationID(sessionID)

	// Assert
	assert.Equal(t, expectedCorrelationID, result)
}

func TestMATLABManager_GetSessionCorrelationID_UnknownSession_ReturnsEmpty(t *testing.T) {
	// Arrange
	mockMATLABServices := &mocks.MockMATLABServices{}
	defer mockMATLABServices.AssertExpectations(t)

	mockSessionStore := &mocks.MockMATLABSessionStore{}
	defer mockSessionStore.AssertExpectations(t)

	mockClientFactory := &mocks.MockMATLABSessionClientFactory{}
	defer mockClientFactory.AssertExpectations(t)

	mockSessionSelector := &mocks.MockSessionSelector{}
	defer mockSessionSelector.AssertExpectations(t)

	mockConfigFactory := &mocks.MockConfigFactory{}
	defer mockConfigFactory.AssertExpectations(t)

	mockClientInfoProvider := &mocks.MockMCPClientInfoProvider{}
	defer mockClientInfoProvider.AssertExpectations(t)

	mockConnectionIndicator := &mocks.MockConnectionIndicator{}
	defer mockConnectionIndicator.AssertExpectations(t)

	unknownSessionID := entities.SessionID(999)

	mockSessionStore.EXPECT().
		CorrelationID(unknownSessionID).
		Return("").
		Once()

	manager := matlabmanager.New(mockConfigFactory, mockMATLABServices, mockSessionStore, mockClientFactory, mockSessionSelector, mockClientInfoProvider, mockConnectionIndicator)

	// Act
	result := manager.GetSessionCorrelationID(unknownSessionID)

	// Assert
	assert.Empty(t, result)
}
