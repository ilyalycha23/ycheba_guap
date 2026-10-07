// Copyright 2026 The MathWorks, Inc.

//go:build darwin

package os

import (
	"strings"
)

func (o OS) Version() (string, error) {
	cmd := o.osLayer.Command("sw_vers", "-productVersion")
	output, err := cmd.Output()
	if err != nil {
		return "", err
	}

	version := strings.TrimSpace(string(output))
	return "macOS " + version, nil
}
