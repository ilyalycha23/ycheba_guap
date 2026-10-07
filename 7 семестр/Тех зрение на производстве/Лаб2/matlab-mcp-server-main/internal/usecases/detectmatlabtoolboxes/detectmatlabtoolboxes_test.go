// Copyright 2025-2026 The MathWorks, Inc.

package detectmatlabtoolboxes_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/testutils"
	"github.com/matlab/matlab-mcp-server/internal/usecases/detectmatlabtoolboxes"
	entitiesmocks "github.com/matlab/matlab-mcp-server/mocks/entities"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestNew_HappyPath(t *testing.T) {
	// Arrange

	// Act
	usecase := detectmatlabtoolboxes.New()

	// Assert
	assert.NotNil(t, usecase, "Usecase should not be nil")
}

func TestUsecase_Execute_HappyPath(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockClient := &entitiesmocks.MockMATLABSessionClient{}
	defer mockClient.AssertExpectations(t)

	evalRequest := entities.EvalRequest{
		Code: "ver",
	}

	evalResponse := entities.EvalResponse{
		ConsoleOutput: "Toolbox list",
		Images:        nil,
	}

	expectedResponse := detectmatlabtoolboxes.ReturnArgs{
		Toolboxes: evalResponse.ConsoleOutput,
	}

	ctx := t.Context()

	mockClient.EXPECT().
		Eval(ctx, mockLogger.AsMockArg(), evalRequest).
		Return(evalResponse, nil).
		Once()

	usecase := detectmatlabtoolboxes.New()

	// Act
	response, err := usecase.Execute(ctx, mockLogger, mockClient)

	// Assert
	require.NoError(t, err, "Execute should not return an error")
	assert.Equal(t, expectedResponse, response, "Response should match expected value")
}

func TestUsecase_Execute_EvalError(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockClient := &entitiesmocks.MockMATLABSessionClient{}
	defer mockClient.AssertExpectations(t)

	evalRequest := entities.EvalRequest{
		Code: "ver",
	}

	expectedError := assert.AnError

	ctx := t.Context()

	mockClient.EXPECT().
		Eval(ctx, mockLogger.AsMockArg(), evalRequest).
		Return(entities.EvalResponse{ConsoleOutput: "some output that shouldn't be because there's an error"}, expectedError).
		Once()

	usecase := detectmatlabtoolboxes.New()

	// Act
	response, err := usecase.Execute(ctx, mockLogger, mockClient)

	// Assert
	require.ErrorIs(t, err, expectedError, "Error should be the original error")
	assert.Empty(t, response, "Response should be empty when there's an error")
}
