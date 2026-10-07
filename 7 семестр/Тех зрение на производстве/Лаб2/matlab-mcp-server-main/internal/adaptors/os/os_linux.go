// Copyright 2026 The MathWorks, Inc.

//go:build linux

package os

import (
	"bufio"
	"path/filepath"
	"strings"
)

func (o OS) Version() (string, error) {
	file, err := o.osLayer.Open(filepath.Join("/etc", "os-release"))
	if err != nil {
		return "", err
	}
	defer func() { _ = file.Close() }()

	var name, version string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, "NAME=") {
			name = strings.Trim(strings.TrimPrefix(line, "NAME="), "\"")
		} else if strings.HasPrefix(line, "VERSION_ID=") {
			version = strings.Trim(strings.TrimPrefix(line, "VERSION_ID="), "\"")
		}
	}

	if err := scanner.Err(); err != nil {
		return "", err
	}

	if name != "" && version != "" {
		return name + " " + version, nil
	}
	if name != "" {
		return name, nil
	}
	return "Linux", nil
}
