// Copyright 2026 The MathWorks, Inc.

package matlabstring_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/usecases/utils/matlabstring"
	"github.com/stretchr/testify/assert"
)

func TestEscapeSingleQuotes_NoQuotes(t *testing.T) {
	// Arrange
	input := "hello world"
	expectedOutput := "hello world"

	// Act
	result := matlabstring.EscapeSingleQuotes(input)

	// Assert
	assert.Equal(t, expectedOutput, result)
}

func TestEscapeSingleQuotes_SingleQuote(t *testing.T) {
	// Arrange
	input := "it's"
	expectedOutput := "it''s"

	// Act
	result := matlabstring.EscapeSingleQuotes(input)

	// Assert
	assert.Equal(t, expectedOutput, result)
}

func TestEscapeSingleQuotes_MultipleQuotes(t *testing.T) {
	// Arrange
	input := "it's a 'test'"
	expectedOutput := "it''s a ''test''"

	// Act
	result := matlabstring.EscapeSingleQuotes(input)

	// Assert
	assert.Equal(t, expectedOutput, result)
}

func TestEscapeSingleQuotes_EmptyString(t *testing.T) {
	// Arrange
	input := ""
	expectedOutput := ""

	// Act
	result := matlabstring.EscapeSingleQuotes(input)

	// Assert
	assert.Equal(t, expectedOutput, result)
}
