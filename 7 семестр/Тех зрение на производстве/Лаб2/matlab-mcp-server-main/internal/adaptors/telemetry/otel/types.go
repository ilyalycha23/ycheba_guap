// Copyright 2026 The MathWorks, Inc.

package otel

import (
	"go.opentelemetry.io/otel/metric"
	sdkmetric "go.opentelemetry.io/otel/sdk/metric"
)

type MeterProvider interface {
	metric.MeterProvider
}

type MetricExporter interface {
	sdkmetric.Exporter
}

type Meter interface {
	metric.Meter
}
