// Copyright 2026 The MathWorks, Inc.

package main

import (
	"encoding/json"
	"os"
)

// StartupInfo is the JSON structure written by the fake MATLAB executable.
// It captures the process working directory and all command-line arguments.
type StartupInfo struct {
	WorkingDir string   `json:"working_dir"`
	Args       []string `json:"args"`
}

func main() {
	cwd, err := os.Getwd()
	if err != nil {
		os.Exit(1)
	}

	outputFile := os.Getenv("FAKE_MATLAB_OUTPUT_FILE")
	if outputFile == "" {
		return
	}

	info := StartupInfo{
		WorkingDir: cwd,
		Args:       os.Args,
	}

	data, err := json.Marshal(info)
	if err != nil {
		os.Exit(1)
	}

	if err := os.WriteFile(outputFile, data, 0o600); err != nil {
		os.Exit(1)
	}
}
