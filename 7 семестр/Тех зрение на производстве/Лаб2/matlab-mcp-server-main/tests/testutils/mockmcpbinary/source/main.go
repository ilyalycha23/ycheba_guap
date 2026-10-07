// Copyright 2026 The MathWorks, Inc.

package main

import (
	"encoding/json"
	"os"
	"strings"
)

type Invocation struct {
	Args []string `json:"args"`
	Env  []string `json:"env"`
}

func main() {
	outputFile := os.Getenv("MOCK_MCPBINARY_OUTPUT_FILE")
	if outputFile == "" {
		return
	}

	var env []string
	for _, e := range os.Environ() {
		if strings.HasPrefix(e, "__MATLAB_MCP_SERVER_MCPB_") {
			env = append(env, e)
		}
	}

	inv := Invocation{
		Args: os.Args[1:],
		Env:  env,
	}

	data, err := json.Marshal(inv)
	if err != nil {
		os.Exit(1)
	}
	data = append(data, '\n')

	f, err := os.OpenFile(outputFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0o600)
	if err != nil {
		os.Exit(1)
	}
	defer func() { _ = f.Close() }()

	if _, err := f.Write(data); err != nil {
		os.Exit(1)
	}
}
