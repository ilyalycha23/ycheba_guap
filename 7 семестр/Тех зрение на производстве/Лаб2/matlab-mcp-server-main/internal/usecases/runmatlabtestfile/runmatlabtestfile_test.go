// Copyright 2025-2026 The MathWorks, Inc.

package runmatlabtestfile_test

import (
	"fmt"
	"path/filepath"
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/testutils"
	"github.com/matlab/matlab-mcp-server/internal/usecases/runmatlabtestfile"
	entitiesmocks "github.com/matlab/matlab-mcp-server/mocks/entities"
	mocks "github.com/matlab/matlab-mcp-server/mocks/usecases/runmatlabtestfile"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestNew_HappyPath(t *testing.T) {
	// Arrange
	mockPathValidator := &mocks.MockPathValidator{}
	defer mockPathValidator.AssertExpectations(t)

	// Act
	usecase := runmatlabtestfile.New(mockPathValidator)

	// Assert
	assert.NotNil(t, usecase, "Usecase should not be nil")
}

func TestUsecase_Execute_HappyPath(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockPathValidator := &mocks.MockPathValidator{}
	defer mockPathValidator.AssertExpectations(t)

	mockClient := &entitiesmocks.MockMATLABSessionClient{}
	defer mockClient.AssertExpectations(t)

	scriptPath := filepath.Join("some", "path", "to", "testFile.m")

	usecaseRequest := runmatlabtestfile.Args{ScriptPath: scriptPath}

	expectedEvalRequest := entities.EvalRequest{
		Code: fmt.Sprintf("runtests('%s')", scriptPath),
	}

	expectedResponse := entities.EvalResponse{
		ConsoleOutput: "Running typeTests\n....\nDone typeTests",
	}

	mockResponse := entities.EvalResponse{
		ConsoleOutput: "Running typeTests\n....\nDone typeTests",
		Images:        [][]byte{[]byte("image1"), []byte("image2")},
	}

	ctx := t.Context()

	mockPathValidator.EXPECT().
		ValidateMATLABScript(scriptPath).
		Return(scriptPath, nil).
		Once()

	mockClient.EXPECT().
		EvalWithCapture(ctx, mockLogger.AsMockArg(), expectedEvalRequest).
		Return(mockResponse, nil).
		Once()

	usecase := runmatlabtestfile.New(mockPathValidator)

	// Act
	response, err := usecase.Execute(ctx, mockLogger, mockClient, usecaseRequest)

	// Assert
	require.NoError(t, err, "Execute should not return an error")
	assert.Equal(t, expectedResponse, response, "Response should match expected value")
}

func TestUsecase_Execute_EscapesSingleQuotesInPath(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockPathValidator := &mocks.MockPathValidator{}
	defer mockPathValidator.AssertExpectations(t)

	mockClient := &entitiesmocks.MockMATLABSessionClient{}
	defer mockClient.AssertExpectations(t)

	ctx := t.Context()
	scriptPath := filepath.Join("Users", "O'Brien", "testFile.m")
	expectedEscapedPath := "Users" + string(filepath.Separator) + "O''Brien" + string(filepath.Separator) + "testFile.m"

	usecaseRequest := runmatlabtestfile.Args{ScriptPath: scriptPath}

	expectedEvalRequest := entities.EvalRequest{
		Code: fmt.Sprintf("runtests('%s')", expectedEscapedPath),
	}

	expectedResponse := entities.EvalResponse{
		ConsoleOutput: "Running typeTests\n....\nDone typeTests",
	}

	mockResponse := entities.EvalResponse{
		ConsoleOutput: "Running typeTests\n....\nDone typeTests",
		Images:        [][]byte{[]byte("image1"), []byte("image2")},
	}

	mockPathValidator.EXPECT().
		ValidateMATLABScript(scriptPath).
		Return(scriptPath, nil).
		Once()

	mockClient.EXPECT().
		EvalWithCapture(ctx, mockLogger.AsMockArg(), expectedEvalRequest).
		Return(mockResponse, nil).
		Once()

	usecase := runmatlabtestfile.New(mockPathValidator)

	// Act
	response, err := usecase.Execute(ctx, mockLogger, mockClient, usecaseRequest)

	// Assert
	require.NoError(t, err, "Execute should not return an error")
	assert.Equal(t, expectedResponse, response, "Response should match expected value")
}

func TestUsecase_Execute_ValidateMATLABScriptError(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockPathValidator := &mocks.MockPathValidator{}
	defer mockPathValidator.AssertExpectations(t)

	mockClient := &entitiesmocks.MockMATLABSessionClient{}
	defer mockClient.AssertExpectations(t)

	ctx := t.Context()
	expectedError := assert.AnError
	scriptPath := filepath.Join("some", "path", "to", "testFile.m")

	usecaseRequest := runmatlabtestfile.Args{ScriptPath: scriptPath}

	mockPathValidator.EXPECT().
		ValidateMATLABScript(scriptPath).
		Return("", expectedError).
		Once()

	usecase := runmatlabtestfile.New(mockPathValidator)

	// Act
	response, err := usecase.Execute(ctx, mockLogger, mockClient, usecaseRequest)

	// Assert
	require.ErrorIs(t, err, expectedError)
	assert.Empty(t, response, "Response should be empty")
}

func TestUsecase_Execute_RunMATLABTestFileEvalError(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockPathValidator := &mocks.MockPathValidator{}
	defer mockPathValidator.AssertExpectations(t)

	mockClient := &entitiesmocks.MockMATLABSessionClient{}
	defer mockClient.AssertExpectations(t)

	ctx := t.Context()
	expectedError := assert.AnError
	scriptPath := filepath.Join("some", "path", "to", "testFile.m")

	usecaseRequest := runmatlabtestfile.Args{ScriptPath: scriptPath}

	expectedEvalRequest := entities.EvalRequest{
		Code: fmt.Sprintf("runtests('%s')", scriptPath),
	}

	mockPathValidator.EXPECT().
		ValidateMATLABScript(scriptPath).
		Return(scriptPath, nil).
		Once()

	mockClient.EXPECT().
		EvalWithCapture(ctx, mockLogger.AsMockArg(), expectedEvalRequest).
		Return(entities.EvalResponse{}, expectedError).
		Once()

	usecase := runmatlabtestfile.New(mockPathValidator)

	// Act
	response, err := usecase.Execute(ctx, mockLogger, mockClient, usecaseRequest)

	// Assert
	require.ErrorIs(t, err, expectedError)
	assert.Empty(t, response, "Response should be empty")
}
