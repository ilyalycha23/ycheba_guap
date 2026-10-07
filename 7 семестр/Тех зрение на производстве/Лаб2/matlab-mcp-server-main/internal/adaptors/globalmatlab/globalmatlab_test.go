// Copyright 2025-2026 The MathWorks, Inc.

package globalmatlab_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/globalmatlab"
	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/testutils"
	mocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/globalmatlab"
	"github.com/stretchr/testify/assert"
)

func TestNew_HappyPath(t *testing.T) {
	// Arrange
	mockMATLABManagerAdaptor := &mocks.MockMATLABManagerAdaptor{}
	defer mockMATLABManagerAdaptor.AssertExpectations(t)

	mockLoggerFactory := &mocks.MockLoggerFactory{}
	defer mockLoggerFactory.AssertExpectations(t)

	// Act
	globalMATLAB := globalmatlab.New(mockMATLABManagerAdaptor, mockLoggerFactory)

	// Assert
	assert.NotNil(t, globalMATLAB)
}

func TestGlobalMATLAB_CurrentCorrelationID_NoSession_ReturnsEmpty(t *testing.T) {
	// Arrange
	mockMATLABManagerAdaptor := &mocks.MockMATLABManagerAdaptor{}
	defer mockMATLABManagerAdaptor.AssertExpectations(t)

	mockLoggerFactory := &mocks.MockLoggerFactory{}
	defer mockLoggerFactory.AssertExpectations(t)

	mockLoggerFactory.EXPECT().
		GetGlobalLogger().
		Return(testutils.NewInspectableLogger(), nil).
		Once()

	ctx := t.Context()

	globalMATLAB := globalmatlab.New(mockMATLABManagerAdaptor, mockLoggerFactory)

	// Act
	result := globalMATLAB.CurrentCorrelationID(ctx)

	// Assert
	assert.Empty(t, result, "no session started means no correlation ID and no adaptor call")
}

func TestGlobalMATLAB_CurrentCorrelationID_HappyPath(t *testing.T) {
	// Arrange
	mockMATLABManagerAdaptor := &mocks.MockMATLABManagerAdaptor{}
	defer mockMATLABManagerAdaptor.AssertExpectations(t)

	mockLoggerFactory := &mocks.MockLoggerFactory{}
	defer mockLoggerFactory.AssertExpectations(t)

	sessionID := entities.SessionID(11)
	expectedCorrelationID := "corr-xyz"

	mockMATLABManagerAdaptor.EXPECT().
		GetSessionCorrelationID(sessionID).
		Return(expectedCorrelationID).
		Once()

	ctx := t.Context()

	globalMATLAB := globalmatlab.New(mockMATLABManagerAdaptor, mockLoggerFactory)
	globalMATLAB.SetSessionIDForTesting(sessionID)

	// Act
	result := globalMATLAB.CurrentCorrelationID(ctx)

	// Assert
	assert.Equal(t, expectedCorrelationID, result)
}
