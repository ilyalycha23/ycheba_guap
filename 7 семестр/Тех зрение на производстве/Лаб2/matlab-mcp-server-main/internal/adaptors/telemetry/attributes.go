// Copyright 2026 The MathWorks, Inc.

package telemetry

import (
	"errors"

	"github.com/matlab/matlab-mcp-server/internal/entities"
	"go.opentelemetry.io/otel/attribute"
)

var (
	ErrEmptyKey     = errors.New("attribute key cannot be empty")
	ErrDuplicateKey = errors.New("attribute key already exists")
)

type Attributes struct {
	logger entities.Logger
	attrs  []attribute.KeyValue
	keys   map[string]struct{}
}

func NewAttributes(logger entities.Logger) *Attributes {
	return &Attributes{
		logger: logger,
		attrs:  make([]attribute.KeyValue, 0),
		keys:   make(map[string]struct{}),
	}
}

func (a *Attributes) AddString(key, value string) {
	if err := a.validateKey(key); err != nil {
		a.logger.WithError(err).Debug("Failed to add " + key + " attribute")
		return
	}
	a.attrs = append(a.attrs, attribute.String(key, value))
	a.trackKey(key)
}

func (a *Attributes) AddInt64(key string, value int64) {
	if err := a.validateKey(key); err != nil {
		a.logger.WithError(err).Debug("Failed to add " + key + " attribute")
		return
	}
	a.attrs = append(a.attrs, attribute.Int64(key, value))
	a.trackKey(key)
}

func (a *Attributes) AddFloat64(key string, value float64) {
	if err := a.validateKey(key); err != nil {
		a.logger.WithError(err).Debug("Failed to add " + key + " attribute")
		return
	}
	a.attrs = append(a.attrs, attribute.Float64(key, value))
	a.trackKey(key)
}

func (a *Attributes) AddBool(key string, value bool) {
	if err := a.validateKey(key); err != nil {
		a.logger.WithError(err).Debug("Failed to add " + key + " attribute")
		return
	}
	a.attrs = append(a.attrs, attribute.Bool(key, value))
	a.trackKey(key)
}

func (a *Attributes) AddStringSlice(key string, value []string) {
	if err := a.validateKey(key); err != nil {
		a.logger.WithError(err).Debug("Failed to add " + key + " attribute")
		return
	}
	a.attrs = append(a.attrs, attribute.StringSlice(key, value))
	a.trackKey(key)
}

func (a *Attributes) AsOTEL() []attribute.KeyValue {
	return a.attrs
}

func (a *Attributes) validateKey(key string) error {
	if key == "" {
		return ErrEmptyKey
	}
	if _, exists := a.keys[key]; exists {
		return ErrDuplicateKey
	}
	return nil
}

func (a *Attributes) trackKey(key string) {
	a.keys[key] = struct{}{}
}
