// Copyright 2025-2026 The MathWorks, Inc.

package listavailablematlabs_test

import (
	"path/filepath"
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/testutils"
	"github.com/matlab/matlab-mcp-server/internal/usecases/listavailablematlabs"
	entitiesmocks "github.com/matlab/matlab-mcp-server/mocks/entities"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
	"github.com/stretchr/testify/require"
)

func TestNew_HappyPath(t *testing.T) {
	// Arrange
	mockMATLABManager := &entitiesmocks.MockMATLABManager{}
	defer mockMATLABManager.AssertExpectations(t)

	// Act
	usecase := listavailablematlabs.New(mockMATLABManager)

	// Assert
	assert.NotNil(t, usecase, "Usecase should not be nil")
}

func TestUsecase_Execute_HappyPath(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockMATLABManager := &entitiesmocks.MockMATLABManager{}
	defer mockMATLABManager.AssertExpectations(t)

	mockEnvironments := []entities.EnvironmentInfo{
		{
			MATLABRoot: filepath.Join("path", "to", "matlab", "R2023a"),
			Version:    "R2023a",
		},
		{
			MATLABRoot: filepath.Join("path", "to", "matlab", "R2022b"),
			Version:    "R2022b",
		},
	}

	mockMATLABManager.EXPECT().
		ListEnvironments(mock.Anything, mockLogger.AsMockArg()).
		Return(mockEnvironments).
		Once()

	usecase := listavailablematlabs.New(mockMATLABManager)
	ctx := t.Context()

	// Act
	result := usecase.Execute(ctx, mockLogger)

	// Assert
	require.Len(t, result, len(mockEnvironments))

	for i := range mockEnvironments {
		assert.Equal(t, mockEnvironments[i].MATLABRoot, result[i].MATLABRoot, "Output MATLAB root does not match input dummy MATLAB root")
		assert.Equal(t, mockEnvironments[i].Version, result[i].Version, "Output MATLAB version does not match input dummy MATLAB version")
	}
}
