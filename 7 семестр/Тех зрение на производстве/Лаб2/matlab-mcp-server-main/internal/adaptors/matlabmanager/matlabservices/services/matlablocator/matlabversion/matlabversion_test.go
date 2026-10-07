// Copyright 2025-2026 The MathWorks, Inc.

package matlabversion_test

import (
	"fmt"
	"path/filepath"
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/matlabmanager/matlabservices/customerrors"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/matlabmanager/matlabservices/datatypes"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/matlabmanager/matlabservices/services/matlablocator/matlabversion"
	mocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/matlabmanager/matlabservices/services/matlablocator/matlabversion"
	osfacademocks "github.com/matlab/matlab-mcp-server/mocks/facades/osfacade"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func newVersionInfo(release, description string) []byte {
	const xmlFormat = `<?xml version="1.0" encoding="UTF-8"?>
<MathWorks_version_info>
	<version>9.14.0</version>
	<release>%s</release>
	<description>%s</description>
	<date>Mar 01 2023</date>
	<checksum>123456</checksum>
</MathWorks_version_info>`

	return []byte(fmt.Sprintf(xmlFormat, release, description))
}

// TestMATLABVersionGetter_Get_HappyPath ensures that the version information is parsed
// correctly in a number of scenarios
func TestMATLABVersionGetter_Get_HappyPath(t *testing.T) {
	testCases := []struct {
		Name                  string
		Release               string
		Description           string
		ExpectedReleaseFamily string
		ExpectedReleasePhase  string
		ExpectedUpdateLevel   int
	}{{ // R2023a GR
		Name:                  "R2023a GR",
		Release:               "R2023a",
		Description:           "",
		ExpectedReleaseFamily: "R2023a",
		ExpectedReleasePhase:  "Release",
		ExpectedUpdateLevel:   0,
	}, { // R2024a Update 3
		Name:                  "R2024a Update 3",
		Release:               "R2024a",
		Description:           "Update 3",
		ExpectedReleaseFamily: "R2024a",
		ExpectedReleasePhase:  "Release",
		ExpectedUpdateLevel:   3,
	}, { // 2025a Prerelease Update 2
		Name:                  "2025a Prerelease Update 2",
		Release:               "2025a",
		Description:           "Prerelease Update 2",
		ExpectedReleaseFamily: "2025a",
		ExpectedReleasePhase:  "Prerelease",
		ExpectedUpdateLevel:   2,
	}}

	for _, tc := range testCases {
		t.Run(tc.Name, func(t *testing.T) {
			// Arrange
			mockOSLayer := &mocks.MockOSLayer{}
			defer mockOSLayer.AssertExpectations(t)

			mockIOLayer := &mocks.MockIOLayer{}
			defer mockIOLayer.AssertExpectations(t)

			mockFile := &osfacademocks.MockFile{}
			defer mockFile.AssertExpectations(t)

			matlabRootLocation := filepath.FromSlash("/path/to/matlab/R2023a")
			versionInfoPath := filepath.FromSlash("/path/to/matlab/R2023a/VersionInfo.xml")

			mockOSLayer.EXPECT().
				Open(versionInfoPath).
				Return(mockFile, nil).
				Once()

			mockFile.EXPECT().
				Close().
				Return(nil).
				Once()

			xmlContent := newVersionInfo(tc.Release, tc.Description)
			mockIOLayer.EXPECT().
				ReadAll(mockFile).
				Return(xmlContent, nil).
				Once()

			service := matlabversion.New(mockOSLayer, mockIOLayer)

			// Act
			result, err := service.Get(matlabRootLocation)

			// Assert
			require.NoError(t, err, "Error should be nil")
			assert.Equal(t, tc.ExpectedReleaseFamily, result.ReleaseFamily, "Release family should match")
			assert.Equal(t, tc.ExpectedReleasePhase, result.ReleasePhase, "Release phase should be 'Release'")
			assert.Equal(t, tc.ExpectedUpdateLevel, result.UpdateLevel, "Update level should be 0")
		})
	}
}

func TestMATLABVersionGetter_Get_HandlesEmptyLocation(t *testing.T) {
	// Arrange
	mockOSLayer := &mocks.MockOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockIOLayer := &mocks.MockIOLayer{}
	defer mockIOLayer.AssertExpectations(t)

	const emptyRoot = ""

	service := matlabversion.New(mockOSLayer, mockIOLayer)

	// Act
	result, err := service.Get(emptyRoot)

	// Assert
	assert.Equal(t, datatypes.MatlabVersionInfo{}, result, "Should return empty version info on empty path")
	require.Error(t, err)
	assert.Equal(t, customerrors.ErrEmptyLocation, err)
}

func TestMATLABVersionGetter_Get_FileOpenError(t *testing.T) {
	// Arrange
	mockOSLayer := &mocks.MockOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockIOLayer := &mocks.MockIOLayer{}
	defer mockIOLayer.AssertExpectations(t)

	matlabRootLocation := filepath.FromSlash("/path/to/matlab/R2023a")
	versionInfoPath := filepath.FromSlash("/path/to/matlab/R2023a/VersionInfo.xml")

	expectedError := assert.AnError
	mockOSLayer.EXPECT().
		Open(versionInfoPath).
		Return(nil, expectedError).
		Once()

	service := matlabversion.New(mockOSLayer, mockIOLayer)

	// Act
	result, err := service.Get(matlabRootLocation)

	// Assert
	require.Error(t, err)
	assert.Equal(t, expectedError, err)
	assert.Equal(t, datatypes.MatlabVersionInfo{}, result, "Should return empty version info on file open error")
}

func TestMATLABVersionGetter_Get_ReadError(t *testing.T) {
	// Arrange
	mockOSLayer := &mocks.MockOSLayer{}
	defer mockOSLayer.AssertExpectations(t)

	mockIOLayer := &mocks.MockIOLayer{}
	defer mockIOLayer.AssertExpectations(t)

	mockFile := &osfacademocks.MockFile{}
	defer mockFile.AssertExpectations(t)

	matlabRootLocation := filepath.FromSlash("/path/to/matlab/R2023a")
	versionInfoPath := filepath.FromSlash("/path/to/matlab/R2023a/VersionInfo.xml")

	mockOSLayer.EXPECT().
		Open(versionInfoPath).
		Return(mockFile, nil).
		Once()

	mockFile.EXPECT().
		Close().
		Return(nil).
		Once()

	expectedError := assert.AnError
	mockIOLayer.EXPECT().
		ReadAll(mockFile).
		Return(nil, expectedError).
		Once()

	service := matlabversion.New(mockOSLayer, mockIOLayer)

	// Act
	result, err := service.Get(matlabRootLocation)

	// Assert
	require.Error(t, err)
	assert.Equal(t, expectedError, err)
	assert.Equal(t, datatypes.MatlabVersionInfo{}, result, "Should return empty version info on read error")
}
