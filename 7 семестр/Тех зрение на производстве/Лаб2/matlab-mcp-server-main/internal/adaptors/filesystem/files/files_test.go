// Copyright 2025-2026 The MathWorks, Inc.

package files_test

import (
	"path/filepath"
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/filesystem/files"
	filesmock "github.com/matlab/matlab-mcp-server/mocks/adaptors/filesystem/files"
	osfacademocks "github.com/matlab/matlab-mcp-server/mocks/facades/osfacade"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestNewFactory_HappyPath(t *testing.T) {
	// Arrange
	mockOSLayer := &filesmock.MockOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	// Act
	factory := files.NewFactory(mockOSLayer)

	// Assert
	assert.NotNil(t, factory, "Factory instance should not be nil")
}

func TestFactory_CreateFileWithUniqueSuffix_HappyPath(t *testing.T) {
	// Arrange
	mockOSLayer := &filesmock.MockOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockFile := &osfacademocks.MockFile{}
	defer mockFile.AssertExpectations(t)

	expectedDir := filepath.Join("tmp", "dir")
	pattern := "testfile"
	expectedTempPattern := "testfile-*"
	expectedFileName := filepath.Join("tmp", "dir", "testfile-1337")
	expectedSuffix := "1337"

	mockOSLayer.EXPECT().
		CreateTemp(expectedDir, expectedTempPattern).
		Return(mockFile, nil).
		Once()

	mockFile.EXPECT().
		Name().
		Return(expectedFileName).
		Once()

	mockFile.EXPECT().
		Close().
		Return(nil).
		Once()

	factory := files.NewFactory(mockOSLayer)

	// Act
	fileName, suffix, err := factory.CreateFileWithUniqueSuffix(filepath.Join(expectedDir, pattern), "")

	// Assert
	require.NoError(t, err, "CreateFileWithUniqueSuffix should not return an error")
	assert.Equal(t, expectedFileName, fileName, "File name should match expected")
	assert.Equal(t, expectedSuffix, suffix, "Suffix should match expected")
}

func TestFactory_CreateFileWithUniqueSuffix_PatternAlreadyHasSeparator(t *testing.T) {
	// Arrange
	mockOSLayer := &filesmock.MockOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockFile := &osfacademocks.MockFile{}
	defer mockFile.AssertExpectations(t)

	expectedDir := filepath.Join("tmp", "dir")
	pattern := "testfile-"
	expectedTempPattern := "testfile-*"
	expectedFileName := filepath.Join("tmp", "dir", "testfile-1337")
	expectedSuffix := "1337"

	mockOSLayer.EXPECT().
		CreateTemp(expectedDir, expectedTempPattern).
		Return(mockFile, nil).
		Once()

	mockFile.EXPECT().
		Name().
		Return(expectedFileName).
		Once()

	mockFile.EXPECT().
		Close().
		Return(nil).
		Once()

	factory := files.NewFactory(mockOSLayer)

	// Act
	fileName, suffix, err := factory.CreateFileWithUniqueSuffix(filepath.Join(expectedDir, pattern), "")

	// Assert
	require.NoError(t, err, "CreateFileWithUniqueSuffix should not return an error")
	assert.Equal(t, expectedFileName, fileName, "File name should match expected")
	assert.Equal(t, expectedSuffix, suffix, "Suffix should match expected")
}

func TestFactory_CreateFileWithUniqueSuffix_FileWithExtension(t *testing.T) {
	// Arrange
	mockOSLayer := &filesmock.MockOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockFile := &osfacademocks.MockFile{}
	defer mockFile.AssertExpectations(t)

	expectedDir := filepath.Join("var", "log", "app")
	pattern := "logfile"
	extension := ".log"
	expectedTempPattern := "logfile-*.log"
	expectedFileName := filepath.Join("var", "log", "app", "logfile-1337.log")
	expectedSuffix := "1337"

	mockOSLayer.EXPECT().
		CreateTemp(expectedDir, expectedTempPattern).
		Return(mockFile, nil).
		Once()

	mockFile.EXPECT().
		Name().
		Return(expectedFileName).
		Once()

	mockFile.EXPECT().
		Close().
		Return(nil).
		Once()

	factory := files.NewFactory(mockOSLayer)

	// Act
	fileName, suffix, err := factory.CreateFileWithUniqueSuffix(filepath.Join(expectedDir, pattern), extension)

	// Assert
	require.NoError(t, err, "CreateFileWithUniqueSuffix should not return an error")
	assert.Equal(t, expectedFileName, fileName, "File name should match expected")
	assert.Equal(t, expectedSuffix, suffix, "Suffix should match expected")
}

func TestFactory_CreateFileWithUniqueSuffix_CreateTempError(t *testing.T) {
	// Arrange
	mockOSLayer := &filesmock.MockOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	expectedDir := filepath.Join("tmp", "dir")
	pattern := "testfile"
	expectedTempPattern := "testfile-*"
	expectedError := assert.AnError

	mockOSLayer.EXPECT().
		CreateTemp(expectedDir, expectedTempPattern).
		Return(nil, expectedError).
		Once()

	factory := files.NewFactory(mockOSLayer)

	// Act
	fileName, suffix, err := factory.CreateFileWithUniqueSuffix(filepath.Join(expectedDir, pattern), "")

	// Assert
	require.ErrorIs(t, err, expectedError, "Error should be the CreateTemp error")
	assert.Empty(t, fileName, "File name should be empty on error")
	assert.Empty(t, suffix, "Suffix should be empty on error")
}

func TestFactory_CreateFileWithUniqueSuffix_CloseError(t *testing.T) {
	// Arrange
	mockOSLayer := &filesmock.MockOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockFile := &osfacademocks.MockFile{}
	defer mockFile.AssertExpectations(t)

	expectedDir := filepath.Join("tmp", "dir")
	pattern := "testfile"
	expectedTempPattern := "testfile-*"
	expectedError := assert.AnError

	mockOSLayer.EXPECT().
		CreateTemp(expectedDir, expectedTempPattern).
		Return(mockFile, nil).
		Once()

	mockFile.EXPECT().
		Close().
		Return(expectedError).
		Once()

	factory := files.NewFactory(mockOSLayer)

	// Act
	fileName, suffix, err := factory.CreateFileWithUniqueSuffix(filepath.Join(expectedDir, pattern), "")

	// Assert
	require.ErrorIs(t, err, expectedError, "Error should be the Close error")
	assert.Empty(t, fileName, "File name should be empty on error")
	assert.Empty(t, suffix, "Suffix should be empty on error")
}

func TestFactory_FilenameWithSuffix_RegularFile(t *testing.T) {
	// Arrange
	mockOSLayer := &filesmock.MockOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	factory := files.NewFactory(mockOSLayer)

	fileName := filepath.Join("path", "to", "file")
	extension := ".txt"
	suffix := "1337"
	expectedResult := filepath.Join("path", "to", "file-1337.txt")

	// Act
	result := factory.FilenameWithSuffix(fileName, extension, suffix)

	// Assert
	assert.Equal(t, expectedResult, result, "Filename with suffix should match expected")
}

func TestFactory_FilenameWithSuffix_HiddenFile(t *testing.T) {
	// Arrange
	mockOSLayer := &filesmock.MockOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	factory := files.NewFactory(mockOSLayer)

	fileName := filepath.Join("path", "to", ".hiddenfile")
	suffix := "1337"
	expectedResult := filepath.Join("path", "to", ".hiddenfile-1337")

	// Act
	result := factory.FilenameWithSuffix(fileName, "", suffix)

	// Assert
	assert.Equal(t, expectedResult, result, "Hidden filename with suffix should match expected")
}

func TestFactory_FilenameWithSuffix_FileWithoutExtension(t *testing.T) {
	// Arrange
	mockOSLayer := &filesmock.MockOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	factory := files.NewFactory(mockOSLayer)

	fileName := filepath.Join("path", "to", "file")
	suffix := "abc"
	expectedResult := filepath.Join("path", "to", "file-abc")

	// Act
	result := factory.FilenameWithSuffix(fileName, "", suffix)

	// Assert
	assert.Equal(t, expectedResult, result, "Filename without extension with suffix should match expected")
}
