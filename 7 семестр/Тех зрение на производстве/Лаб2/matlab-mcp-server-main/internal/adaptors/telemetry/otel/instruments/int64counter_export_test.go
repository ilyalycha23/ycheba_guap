// Copyright 2026 The MathWorks, Inc.

package instruments

import "go.opentelemetry.io/otel/metric"

func NewInt64CounterForTesting(meter metric.Meter, name, description, unit string) (Int64Counter, error) {
	return newInt64Counter(meter, name, description, unit)
}
