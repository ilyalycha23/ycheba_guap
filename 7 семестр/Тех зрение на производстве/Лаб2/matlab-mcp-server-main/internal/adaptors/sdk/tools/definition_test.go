// Copyright 2026 The MathWorks, Inc.

package tools_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/tools"
	"github.com/stretchr/testify/require"
)

func TestNewDefinition_HappyPath(t *testing.T) {
	// Arrange
	expectedName := "test-tool"
	expectedTitle := "Test Tool"
	expectedDescription := "A test tool"
	expectedAnnotations := tools.NewReadOnlyAnnotations()

	// Act
	definition := tools.NewDefinition(expectedName, expectedTitle, expectedDescription, expectedAnnotations)

	// Assert
	require.Equal(t, expectedName, definition.Name)
	require.Equal(t, expectedTitle, definition.Title)
	require.Equal(t, expectedDescription, definition.Description)
	require.Equal(t, expectedAnnotations, definition.Annotations)
}

func TestNewDefinition_NilAnnotations(t *testing.T) {
	// Arrange
	expectedName := "test-tool"
	expectedTitle := "Test Tool"
	expectedDescription := "A test tool"

	// Act
	definition := tools.NewDefinition(expectedName, expectedTitle, expectedDescription, nil)

	// Assert
	require.NotNil(t, definition.Annotations)
	require.Equal(t, tools.NewReadOnlyAnnotations(), definition.Annotations)
}
