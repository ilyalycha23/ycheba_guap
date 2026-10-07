// Copyright 2025-2026 The MathWorks, Inc.

package instruments

import (
	"context"

	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/metric"
)

type int64Counter struct {
	counter metric.Int64Counter
}

func newInt64Counter(meter metric.Meter, name, description, unit string) (Int64Counter, error) {
	counter, err := meter.Int64Counter(name,
		metric.WithDescription(description),
		metric.WithUnit(unit),
	)
	if err != nil {
		return nil, err
	}

	return &int64Counter{
		counter: counter,
	}, nil
}

func (c *int64Counter) Add(ctx context.Context, value int64, attrs []attribute.KeyValue) {
	options := []metric.AddOption{}
	if attrs != nil {
		options = append(options, metric.WithAttributes(attrs...))
	}

	c.counter.Add(ctx, value, options...)
}
