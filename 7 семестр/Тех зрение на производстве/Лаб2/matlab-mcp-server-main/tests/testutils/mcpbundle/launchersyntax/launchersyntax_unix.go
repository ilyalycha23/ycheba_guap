// Copyright 2026 The MathWorks, Inc.

//go:build !windows

package launchersyntax

import (
	"fmt"
	"os/exec"
)

func Check(path string) error {
	cmd := exec.Command("bash", "-n", path)
	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("syntax errors: %s", output)
	}
	return nil
}
