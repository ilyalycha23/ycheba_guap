// Copyright 2026 The MathWorks, Inc.

package main

import "errors"

var (
	ServiceStartErr = &i18nError{ //nolint:gochecknoglobals // This is an error
		error: errors.New("service failed to start"),
	}
)

type i18nError struct {
	error
}

func (e *i18nError) MWMarker() {}
