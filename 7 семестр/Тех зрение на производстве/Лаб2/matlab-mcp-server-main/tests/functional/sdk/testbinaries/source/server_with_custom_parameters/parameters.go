// Copyright 2026 The MathWorks, Inc.

package main

import (
	"github.com/matlab/matlab-mcp-server/pkg/config"
)

func CustomParameter() config.Parameter[string] {
	return config.Parameter[string]{
		ID:           "custom-param-id",
		FlagName:     "custom-param",
		HiddenFlag:   false,
		EnvVarName:   "CUSTOM_PARAM",
		Description:  "A custom parameter for testing",
		DefaultValue: "default-value",
	}
}

func CustomRecordedParameter() config.Parameter[string] {
	return config.Parameter[string]{
		ID:           "custom-recorded-param-id",
		FlagName:     "custom-recorded-param",
		HiddenFlag:   false,
		EnvVarName:   "CUSTOM_RECORDED_PARAM",
		Description:  "A custom recorded parameter for testing",
		DefaultValue: "recorded-default-value",
		RecordToLog:  true,
	}
}
