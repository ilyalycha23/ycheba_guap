// Copyright 2026 The MathWorks, Inc.

package instruments

import (
	"context"

	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/metric"
)

type Int64Counter interface {
	Add(ctx context.Context, value int64, attrs []attribute.KeyValue)
}

type Factory struct{}

func NewFactory() *Factory {
	return &Factory{}
}

func (f *Factory) NewInt64Counter(meter metric.Meter, name, description, unit string) (Int64Counter, error) {
	return newInt64Counter(meter, name, description, unit)
}
