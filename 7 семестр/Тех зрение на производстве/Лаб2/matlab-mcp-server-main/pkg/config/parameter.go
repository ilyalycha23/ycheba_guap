// Copyright 2026 The MathWorks, Inc.

package config

type supportedParameterValueType interface {
	string | bool
}

type Parameter[ValueType supportedParameterValueType] struct {
	ID           string
	FlagName     string
	HiddenFlag   bool
	EnvVarName   string
	Description  string
	DefaultValue ValueType

	RecordToLog bool
	PIISafe     bool
}

func (p Parameter[ValueType]) GetID() string {
	return p.ID
}

func (p Parameter[ValueType]) GetFlagName() string {
	return p.FlagName
}

func (p Parameter[ValueType]) GetHiddenFlag() bool {
	return p.HiddenFlag
}

func (p Parameter[ValueType]) GetEnvVarName() string {
	return p.EnvVarName
}

func (p Parameter[ValueType]) GetDescription() string {
	return p.Description
}

func (p Parameter[ValueType]) GetDefaultValue() any {
	return p.DefaultValue
}

func (p Parameter[ValueType]) GetActive() bool {
	// SDK Parameters are always active
	return true
}

func (p Parameter[ValueType]) GetRecordToLog() bool {
	return p.RecordToLog
}

func (p Parameter[ValueType]) GetPIISafe() bool {
	return p.PIISafe
}
