// Copyright 2026 The MathWorks, Inc.

package testbinaries

type ServerDetails struct {
	binaryLocation string

	moduleName string

	name         string
	title        string
	instructions string
}

func (s ServerDetails) BinaryLocation() string {
	return s.binaryLocation
}

func (s ServerDetails) ModuleName() string {
	return s.moduleName
}

func (s ServerDetails) Name() string {
	return s.name
}

func (s ServerDetails) Title() string {
	return s.title
}

func (s ServerDetails) Instructions() string {
	return s.instructions
}

type ServerWithCustomToolsDetails struct {
	ServerDetails

	greetToolName           string
	greetStructuredToolName string
}

func (s ServerWithCustomToolsDetails) GreetToolName() string {
	return s.greetToolName
}

func (s ServerWithCustomToolsDetails) GreetStructuredToolName() string {
	return s.greetStructuredToolName
}

type ServerWithCustomParametersDetails struct {
	ServerDetails

	greetToolName               string
	greetStructuredToolName     string
	customParamFlagName         string
	customRecordedParamFlagName string
	customRecordedParamID       string
	customRecordedParamEnvVar   string
}

func (s ServerWithCustomParametersDetails) GreetToolName() string {
	return s.greetToolName
}

func (s ServerWithCustomParametersDetails) GreetStructuredToolName() string {
	return s.greetStructuredToolName
}

func (s ServerWithCustomParametersDetails) CustomParamFlagName() string {
	return s.customParamFlagName
}

func (s ServerWithCustomParametersDetails) CustomRecordedParamFlagName() string {
	return s.customRecordedParamFlagName
}

func (s ServerWithCustomParametersDetails) CustomRecordedParamID() string {
	return s.customRecordedParamID
}

func (s ServerWithCustomParametersDetails) CustomRecordedParamEnvVar() string {
	return s.customRecordedParamEnvVar
}

type ServerWithCustomDependenciesDetails struct {
	ServerDetails

	greetToolName string
}

func (s ServerWithCustomDependenciesDetails) GreetToolName() string {
	return s.greetToolName
}

type ServerWithWatchdogDetails struct {
	ServerDetails

	getPIDToolName string
}

func (s ServerWithWatchdogDetails) GetPIDToolName() string {
	return s.getPIDToolName
}

type ServerWithLoggingDetails struct {
	ServerDetails

	toolThatLogsName           string
	structuredToolThatLogsName string
}

func (s ServerWithLoggingDetails) ToolThatLogsName() string {
	return s.toolThatLogsName
}

func (s ServerWithLoggingDetails) StructuredToolThatLogsName() string {
	return s.structuredToolThatLogsName
}
