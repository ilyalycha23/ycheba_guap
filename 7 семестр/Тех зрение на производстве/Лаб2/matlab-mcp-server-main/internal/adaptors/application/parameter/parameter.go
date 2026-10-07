// Copyright 2026 The MathWorks, Inc.

package parameter

import (
	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/messages"
)

type ParameterWithDescriptionFromMessageCatalog interface {
	entities.Parameter
	SetActive(active bool)
	SetDescription(description string)
	GetDescriptionKey() messages.MessageKey
}

type Parameter[ValueType any] struct {
	id             string
	flagName       string
	hiddenFlag     bool
	envVarName     string
	descriptionKey messages.MessageKey
	description    string
	defaultValue   ValueType

	active      bool
	recordToLog bool
	piiSafe     bool
}

func NewParameter[ValueType any](
	id string,
	flagName string,
	hiddenFlag bool,
	envVarName string,
	descriptionKey messages.MessageKey,
	defaultValue ValueType,
	recordToLog bool,
	piiSafe bool,
) *Parameter[ValueType] {
	return &Parameter[ValueType]{
		id:             id,
		flagName:       flagName,
		hiddenFlag:     hiddenFlag,
		envVarName:     envVarName,
		descriptionKey: descriptionKey,
		defaultValue:   defaultValue,

		active:      true,
		recordToLog: recordToLog,
		piiSafe:     piiSafe,
	}
}

func (p Parameter[ValueType]) GetID() string {
	return p.id
}

func (p Parameter[ValueType]) GetFlagName() string {
	return p.flagName
}

func (p Parameter[ValueType]) GetHiddenFlag() bool {
	return p.hiddenFlag
}

func (p Parameter[ValueType]) GetEnvVarName() string {
	return p.envVarName
}

func (p Parameter[ValueType]) GetDescription() string {
	return p.description
}

func (p Parameter[ValueType]) GetDefaultValue() any {
	return p.defaultValue
}

func (p Parameter[ValueType]) GetTypedDefaultValue() ValueType {
	return p.defaultValue
}

func (p *Parameter[ValueType]) SetDescription(description string) {
	p.description = description
}

func (p Parameter[ValueType]) GetDescriptionKey() messages.MessageKey {
	return p.descriptionKey
}

func (p *Parameter[ValueType]) SetActive(active bool) {
	p.active = active
}

func (p Parameter[ValueType]) GetActive() bool {
	return p.active
}

func (p Parameter[ValueType]) GetRecordToLog() bool {
	return p.recordToLog
}

func (p Parameter[ValueType]) GetPIISafe() bool {
	return p.piiSafe
}
