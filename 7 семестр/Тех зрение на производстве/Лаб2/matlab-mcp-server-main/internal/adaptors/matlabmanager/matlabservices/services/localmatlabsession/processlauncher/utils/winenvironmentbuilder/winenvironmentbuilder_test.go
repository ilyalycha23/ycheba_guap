// Copyright 2025-2026 The MathWorks, Inc.
//go:build windows

package winenvironmentbuilder_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/matlabmanager/matlabservices/services/localmatlabsession/processlauncher/utils/winenvironmentbuilder"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestBuild_HappyPath_BasicVariables(t *testing.T) {
	// Arrange
	env := []string{
		"PATH=C:\\Windows",
		"HOME=C:\\Users\\test",
		"SIMPLE=value",
	}
	expectedBlock := winenvironmentbuilder.EncodeEntries([]string{
		"HOME=C:\\Users\\test",
		"PATH=C:\\Windows",
		"SIMPLE=value",
	})

	// Act
	block, err := winenvironmentbuilder.Build(env)

	// Assert
	require.NoError(t, err)
	assert.Equal(t, expectedBlock, block)
}

func TestBuild_HappyPath_EmptyOrNilInput(t *testing.T) {
	testCases := []struct {
		name  string
		input []string
	}{
		{"empty slice", []string{}},
		{"nil", nil},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Arrange

			// Act
			block, err := winenvironmentbuilder.Build(tc.input)

			// Assert
			require.NoError(t, err)
			assert.Nil(t, block)
		})
	}
}

func TestBuild_HappyPath_HiddenWindowsVariables(t *testing.T) {
	testCases := []struct {
		name           string
		entries        []string
		expectedSorted []string
	}{
		{
			name:           "drive variables mixed with regular",
			entries:        []string{"=C:=C:\\Users\\test", "=D:=D:\\Projects", "PATH=C:\\Windows"},
			expectedSorted: []string{"=C:=C:\\Users\\test", "=D:=D:\\Projects", "PATH=C:\\Windows"},
		},
		{
			name:           "UNC path variable",
			entries:        []string{"=::=::\\"}, // name: "=::", value: "::\"
			expectedSorted: []string{"=::=::\\"},
		},
		{
			name:           "ExitCode hidden variable",
			entries:        []string{"=ExitCode=00000000"},
			expectedSorted: []string{"=ExitCode=00000000"},
		},
		{
			name:           "hidden variable with symbols",
			entries:        []string{"=@:=value", "={:=value"},
			expectedSorted: []string{"=@:=value", "={:=value"},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Arrange
			expectedBlock := winenvironmentbuilder.EncodeEntries(tc.expectedSorted)

			// Act
			block, err := winenvironmentbuilder.Build(tc.entries)

			// Assert
			require.NoError(t, err)
			assert.Equal(t, expectedBlock, block)
		})
	}
}

func TestBuild_HappyPath_CaseInsensitiveDeduplication(t *testing.T) {
	// Arrange
	env := []string{
		"path=first",
		"PATH=second",
		"Path=third",
	}
	expectedBlock := winenvironmentbuilder.EncodeEntries([]string{"Path=third"})

	// Act
	block, err := winenvironmentbuilder.Build(env)

	// Assert
	require.NoError(t, err)
	assert.Equal(t, expectedBlock, block)
}

func TestBuild_HappyPath_SortedAlphabetically(t *testing.T) {
	// Arrange
	env := []string{
		"ZEBRA=last",
		"ALPHA=first",
		"MIDDLE=middle",
	}
	expectedBlock := winenvironmentbuilder.EncodeEntries([]string{"ALPHA=first", "MIDDLE=middle", "ZEBRA=last"})

	// Act
	block, err := winenvironmentbuilder.Build(env)

	// Assert
	require.NoError(t, err)
	assert.Equal(t, expectedBlock, block)
}

func TestBuild_HappyPath_EmptyValueAllowed(t *testing.T) {
	// Arrange
	expectedBlock := winenvironmentbuilder.EncodeEntries([]string{"EMPTY_VALUE="})

	// Act
	block, err := winenvironmentbuilder.Build([]string{"EMPTY_VALUE="})

	// Assert
	require.NoError(t, err)
	assert.Equal(t, expectedBlock, block)
}

func TestBuild_HappyPath_ValueWithEquals(t *testing.T) {
	// Arrange
	expectedBlock := winenvironmentbuilder.EncodeEntries([]string{"VAR=value=with=equals"})

	// Act
	block, err := winenvironmentbuilder.Build([]string{"VAR=value=with=equals"})

	// Assert
	require.NoError(t, err)
	assert.Equal(t, expectedBlock, block)
}

func TestBuild_HappyPath_UnicodeCharacters(t *testing.T) {
	// Arrange
	env := []string{
		"UNICODE=日本語",
		"EMOJI=🎉",
		"ACCENTS=café résumé",
	}
	expectedBlock := winenvironmentbuilder.EncodeEntries([]string{
		"ACCENTS=café résumé",
		"EMOJI=🎉",
		"UNICODE=日本語",
	})

	// Act
	block, err := winenvironmentbuilder.Build(env)

	// Assert
	require.NoError(t, err)
	assert.Equal(t, expectedBlock, block)
}

func TestBuild_HappyPath_SpacesInNameAndValue(t *testing.T) {
	// Arrange
	env := []string{
		"VAR WITH SPACES=value with spaces",
		"NORMAL=  leading and trailing spaces  ",
	}
	expectedBlock := winenvironmentbuilder.EncodeEntries([]string{
		"NORMAL=  leading and trailing spaces  ",
		"VAR WITH SPACES=value with spaces",
	})

	// Act
	block, err := winenvironmentbuilder.Build(env)

	// Assert
	require.NoError(t, err)
	assert.Equal(t, expectedBlock, block)
}

func TestBuild_HappyPath_SpecialCharactersInValue(t *testing.T) {
	// Arrange
	env := []string{
		`QUOTES=value with "quotes"`,
		"BACKSLASH=C:\\path\\to\\file",
		"PERCENT=%PATH%",
	}
	expectedBlock := winenvironmentbuilder.EncodeEntries([]string{
		"BACKSLASH=C:\\path\\to\\file",
		"PERCENT=%PATH%",
		`QUOTES=value with "quotes"`,
	})

	// Act
	block, err := winenvironmentbuilder.Build(env)

	// Assert
	require.NoError(t, err)
	assert.Equal(t, expectedBlock, block)
}

func TestBuild_Error_InvalidEntryRejected(t *testing.T) {
	testCases := []struct {
		name        string
		entry       string
		errContains string
	}{
		{"equals alone", "==value", "expected name=value"},
		{"empty name", "=value", "expected name=value"},
		{"no equals sign", "INVALIDENTRY", "expected name=value"},
		{"NUL in value", "VAR=value\x00with\x00nuls", "contains NUL"},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Arrange
			// (invalid input defined in test case)

			// Act
			_, err := winenvironmentbuilder.Build([]string{tc.entry})

			// Assert
			require.Error(t, err)
			assert.Contains(t, err.Error(), tc.errContains)
		})
	}
}
func TestPointerToFirstElement_NilBlock(t *testing.T) {
	// Arrange
	var block winenvironmentbuilder.EnvironmentBlock = nil

	// Act
	ptr := block.PointerToFirstElement()

	// Assert
	assert.Nil(t, ptr)
}

func TestPointerToFirstElement_EmptyBlock(t *testing.T) {
	// Arrange
	block := winenvironmentbuilder.EnvironmentBlock{}

	// Act
	ptr := block.PointerToFirstElement()

	// Assert
	assert.Nil(t, ptr)
}

func TestPointerToFirstElement_BlockWithElements(t *testing.T) {
	// Arrange
	block := winenvironmentbuilder.EncodeEntries([]string{"VAR=value"})

	// Act
	ptr := block.PointerToFirstElement()

	// Assert
	require.NotNil(t, ptr)
	assert.Equal(t, block[0], *ptr)
}
