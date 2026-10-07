// Copyright 2025 The MathWorks, Inc.

package customerrors

import (
	"errors"
)

var (
	ErrEmptyLocation = errors.New("location cannot be empty")
)
