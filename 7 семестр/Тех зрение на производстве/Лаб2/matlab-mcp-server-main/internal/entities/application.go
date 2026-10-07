// Copyright 2026 The MathWorks, Inc.

package entities

type Parameter interface {
	GetID() string
	GetFlagName() string
	GetHiddenFlag() bool
	GetEnvVarName() string
	GetDescription() string
	GetDefaultValue() any

	GetActive() bool
	GetRecordToLog() bool
	GetPIISafe() bool
}
