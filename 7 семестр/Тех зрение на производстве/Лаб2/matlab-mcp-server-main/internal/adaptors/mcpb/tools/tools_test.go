// Copyright 2026 The MathWorks, Inc.

package tools_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/mcpb/tools"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestDefinitions_HappyPath(t *testing.T) {
	// Arrange

	// Act
	var defs []tools.Definition
	require.NotPanics(t, func() {
		defs = tools.Definitions()
	})

	// Assert
	require.Len(t, defs, 5)

	expectedNames := []string{
		"check_matlab_code",
		"detect_matlab_toolboxes",
		"evaluate_matlab_code",
		"run_matlab_file",
		"run_matlab_test_file",
	}

	for i, expectedName := range expectedNames {
		assert.Equal(t, expectedName, defs[i].Name)
		assert.NotEmpty(t, defs[i].Description)
	}
}
