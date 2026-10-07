// Copyright 2026 The MathWorks, Inc.

package config_test

import (
	"testing"

	"github.com/stretchr/testify/assert"

	pkgconfig "github.com/matlab/matlab-mcp-server/pkg/config"
)

func TestParameter_String_HappyPath(t *testing.T) {
	// Arrange
	expectedID := "string-param-id"
	expectedFlagName := "string-flag"
	expectedHiddenFlag := true
	expectedEnvVarName := "STRING_ENV_VAR"
	expectedDescription := "A string parameter"
	expectedDefaultValue := "default-value"
	expectedRecordToLog := true
	expectedPIISafe := false

	param := pkgconfig.Parameter[string]{
		ID:           expectedID,
		FlagName:     expectedFlagName,
		HiddenFlag:   expectedHiddenFlag,
		EnvVarName:   expectedEnvVarName,
		Description:  expectedDescription,
		DefaultValue: expectedDefaultValue,
		RecordToLog:  expectedRecordToLog,
		PIISafe:      expectedPIISafe,
	}

	// Act & Assert
	assert.Equal(t, expectedID, param.GetID())
	assert.Equal(t, expectedFlagName, param.GetFlagName())
	assert.Equal(t, expectedHiddenFlag, param.GetHiddenFlag())
	assert.Equal(t, expectedEnvVarName, param.GetEnvVarName())
	assert.Equal(t, expectedDescription, param.GetDescription())
	assert.Equal(t, expectedDefaultValue, param.GetDefaultValue())
	assert.True(t, param.GetActive())
	assert.Equal(t, expectedRecordToLog, param.GetRecordToLog())
	assert.Equal(t, expectedPIISafe, param.GetPIISafe())
}

func TestParameter_Bool_HappyPath(t *testing.T) {
	// Arrange
	expectedID := "bool-param-id"
	expectedFlagName := "bool-flag"
	expectedHiddenFlag := false
	expectedEnvVarName := "BOOL_ENV_VAR"
	expectedDescription := "A bool parameter"
	expectedDefaultValue := true
	expectedRecordToLog := false
	expectedPIISafe := true

	param := pkgconfig.Parameter[bool]{
		ID:           expectedID,
		FlagName:     expectedFlagName,
		HiddenFlag:   expectedHiddenFlag,
		EnvVarName:   expectedEnvVarName,
		Description:  expectedDescription,
		DefaultValue: expectedDefaultValue,
		RecordToLog:  expectedRecordToLog,
		PIISafe:      expectedPIISafe,
	}

	// Act & Assert
	assert.Equal(t, expectedID, param.GetID())
	assert.Equal(t, expectedFlagName, param.GetFlagName())
	assert.Equal(t, expectedHiddenFlag, param.GetHiddenFlag())
	assert.Equal(t, expectedEnvVarName, param.GetEnvVarName())
	assert.Equal(t, expectedDescription, param.GetDescription())
	assert.Equal(t, expectedDefaultValue, param.GetDefaultValue())
	assert.True(t, param.GetActive())
	assert.Equal(t, expectedRecordToLog, param.GetRecordToLog())
	assert.Equal(t, expectedPIISafe, param.GetPIISafe())
}

func TestParameter_GetActive_AlwaysTrue(t *testing.T) {
	// Arrange
	stringParam := pkgconfig.Parameter[string]{}
	boolParam := pkgconfig.Parameter[bool]{}

	// Act & Assert
	assert.True(t, stringParam.GetActive())
	assert.True(t, boolParam.GetActive())
}
