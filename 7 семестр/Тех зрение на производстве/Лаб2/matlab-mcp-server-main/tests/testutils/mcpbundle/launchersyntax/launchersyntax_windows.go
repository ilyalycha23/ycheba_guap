// Copyright 2026 The MathWorks, Inc.

//go:build windows

package launchersyntax

import (
	"fmt"
	"os"
)

func Check(path string) error {
	info, err := os.Stat(path)
	if err != nil {
		return fmt.Errorf("launcher script not found: %w", err)
	}
	if info.Size() == 0 {
		return fmt.Errorf("launcher script is empty")
	}
	return nil
}
