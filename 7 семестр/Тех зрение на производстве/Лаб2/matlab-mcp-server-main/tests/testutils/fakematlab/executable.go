// Copyright 2026 The MathWorks, Inc.

// This file provides a compilable fake MATLAB executable for functional tests.
//
// How it works:
//  1. CreateExecutable compiles source/main.go into a real binary and sets up
//     a directory layout that the MCP server recognizes as a valid MATLAB installation.
//  2. The test suite injects the FAKE_MATLAB_OUTPUT_FILE env var into the MCP server's
//     environment. The server passes this env through to the MATLAB process it launches.
//  3. When the fake binary starts, it captures its working directory and command-line
//     arguments, writes them as JSON to the file specified by FAKE_MATLAB_OUTPUT_FILE,
//     and exits.
//  4. The test reads the JSON via Installation.ReadStartupInfo() to verify how the
//     MCP server launched MATLAB (e.g., which working directory was used).

package fakematlab

import (
	"encoding/json"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/require"
)

const OutputFileEnvVar = "FAKE_MATLAB_OUTPUT_FILE"

// StartupInfo is the JSON structure written by the fake MATLAB executable.
// It captures the process working directory and all command-line arguments.
type StartupInfo struct {
	WorkingDir string   `json:"working_dir"`
	Args       []string `json:"args"`
}

// Installation holds the paths for a fake MATLAB installation.
type Installation struct {
	Root           string // The MATLAB root directory (e.g., tempdir)
	PathEntry      string // The directory to add to PATH (root/bin)
	OutputFilePath string // Path where the fake writes its startup info as JSON
}

// ReadStartupInfo reads and parses the startup info written by the fake MATLAB executable.
func (i Installation) ReadStartupInfo() (StartupInfo, error) {
	data, err := os.ReadFile(i.OutputFilePath)
	if err != nil {
		return StartupInfo{}, err
	}
	var info StartupInfo
	if err := json.Unmarshal(data, &info); err != nil {
		return StartupInfo{}, err
	}
	return info, nil
}

// CreateExecutable compiles the fake MATLAB source and sets up a full installation layout.
func CreateExecutable(t *testing.T) Installation {
	t.Helper()

	root := t.TempDir()
	binDir := filepath.Join(root, "bin")

	// Resolve the source directory relative to the Go module root.
	goModCmd := exec.Command("go", "env", "GOMOD")
	goModOutput, err := goModCmd.Output()
	require.NoError(t, err)
	moduleRoot := filepath.Dir(strings.TrimSpace(string(goModOutput)))
	sourceDir := filepath.Join(moduleRoot, "tests", "testutils", "fakematlab", "source")

	buildAndInstall(t, sourceDir, root, binDir)

	// Create a minimal VersionInfo.xml so the MATLAB locator accepts this root.
	versionInfoXML := []byte(`<?xml version="1.0" encoding="UTF-8"?>
<MathWorksVersionInfo>
  <release>R2025b</release>
  <description>Update 1</description>
</MathWorksVersionInfo>`)
	err = os.WriteFile(filepath.Join(root, "VersionInfo.xml"), versionInfoXML, 0o600)
	require.NoError(t, err)

	outputFilePath := filepath.Join(root, "startup-working-dir.txt")

	return Installation{
		Root:           root,
		PathEntry:      binDir,
		OutputFilePath: outputFilePath,
	}
}
