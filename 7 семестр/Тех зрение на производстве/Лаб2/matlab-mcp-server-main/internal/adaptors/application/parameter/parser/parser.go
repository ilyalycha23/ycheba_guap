// Copyright 2025-2026 The MathWorks, Inc.

package parser

import (
	"fmt"
	"sort"
	"strings"
	"sync"

	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/messages"
	"github.com/spf13/pflag"
)

type DefaultParameterFactory interface {
	DefaultParameters() []entities.Parameter
}

type ParameterFactory interface {
	Parameters() []entities.Parameter
}

type OSLayer interface {
	LookupEnv(key string) (string, bool)
}

type Parser struct {
	osLayer                 OSLayer
	defaultParameterFactory DefaultParameterFactory
	parameterFactory        ParameterFactory

	flagSet         *pflag.FlagSet
	parameters      []entities.Parameter
	flagToParameter map[string]entities.Parameter

	once      sync.Once
	usageText string
	initErr   messages.Error
}

func New(
	osLayer OSLayer,
	defaultParameterFactory DefaultParameterFactory,
	parameterFactory ParameterFactory,
) *Parser {
	return &Parser{
		osLayer:                 osLayer,
		defaultParameterFactory: defaultParameterFactory,
		parameterFactory:        parameterFactory,
	}
}

func (p *Parser) Usage() (string, messages.Error) {
	if err := p.initialize(); err != nil {
		return "", err
	}

	return p.usageText, nil
}

func (p *Parser) Parse(args []string) ([]entities.Parameter, map[string]any, []string, messages.Error) {
	if err := p.initialize(); err != nil {
		return nil, nil, nil, err
	}

	specifiedArgs := make(map[string]any)
	for _, param := range p.parameters {
		specifiedArgs[param.GetID()] = param.GetDefaultValue()
	}

	specifiedParameters := map[string]struct{}{}

	if err := p.parseEnvVars(specifiedArgs, specifiedParameters); err != nil {
		return nil, nil, nil, err
	}

	if err := p.parseFlags(args, specifiedArgs, specifiedParameters); err != nil {
		return nil, nil, nil, err
	}

	specifiedIDs := make([]string, 0, len(specifiedParameters))
	for id := range specifiedParameters {
		specifiedIDs = append(specifiedIDs, id)
	}
	sort.Strings(specifiedIDs)

	return p.parameters, specifiedArgs, specifiedIDs, nil
}

func (p *Parser) initialize() messages.Error {
	p.once.Do(func() {
		allParameters, err := p.allParameters()
		if err != nil {
			p.initErr = err
			return
		}

		p.parameters = allParameters
		p.flagToParameter = make(map[string]entities.Parameter)
		for _, param := range allParameters {
			if flagName := param.GetFlagName(); flagName != "" {
				p.flagToParameter[flagName] = param
			}
		}

		p.flagSet = pflag.NewFlagSet(pflag.CommandLine.Name(), pflag.ContinueOnError)
		p.setupFlags()
		p.generateUsageText()
	})
	return p.initErr
}

func (p *Parser) allParameters() ([]entities.Parameter, messages.Error) {
	allParams := append(p.defaultParameterFactory.DefaultParameters(), p.parameterFactory.Parameters()...)

	seenIDs := make(map[string]struct{})
	seenFlags := make(map[string]struct{})
	seenEnvVars := make(map[string]struct{})

	for _, param := range allParams {
		id := param.GetID()
		if id == "" {
			return nil, messages.New_StartupErrors_InvalidParameterKey_Error(id)
		}

		if _, ok := seenIDs[id]; ok {
			return nil, messages.New_StartupErrors_DuplicateParameter_Error(id, "parameter ID", id)
		}
		seenIDs[id] = struct{}{}

		flag := param.GetFlagName()
		if flag != "" {
			if _, ok := seenFlags[flag]; ok {
				return nil, messages.New_StartupErrors_DuplicateParameter_Error(id, "flag name", flag)
			}
			seenFlags[flag] = struct{}{}
		}

		envVar := strings.ToUpper(param.GetEnvVarName())
		if envVar != "" {
			if _, ok := seenEnvVars[envVar]; ok {
				return nil, messages.New_StartupErrors_DuplicateParameter_Error(id, "env var name", envVar)
			}
			seenEnvVars[envVar] = struct{}{}
		}
	}

	return allParams, nil
}

func (p *Parser) generateUsageText() {
	usageText := fmt.Sprintf("%s\n", "Usage:")

	// Determine max flag length
	maxFlagLength := 0
	prePadding := 6
	postPadding := 2

	p.flagSet.VisitAll(func(f *pflag.Flag) {
		if f.Hidden {
			return
		}
		if len(f.Name) > maxFlagLength {
			maxFlagLength = len(f.Name)
		}
	})

	p.flagSet.VisitAll(func(f *pflag.Flag) {
		if f.Hidden {
			return
		}
		padding := maxFlagLength + postPadding + 2 - len(f.Name)
		usageText += fmt.Sprintf("%s--%s%s%s\n", strings.Repeat(" ", prePadding), f.Name, strings.Repeat(" ", padding), f.Usage)
	})

	p.usageText = usageText
}
