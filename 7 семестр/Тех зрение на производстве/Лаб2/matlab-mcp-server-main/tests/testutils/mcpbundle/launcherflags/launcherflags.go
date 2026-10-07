// Copyright 2026 The MathWorks, Inc.

package launcherflags

import (
	"regexp"
	"sort"
	"strings"
)

var flagRegex = regexp.MustCompile(`__MATLAB_MCP_SERVER_MCPB_\w+:(string|bool):(--[a-z][a-z0-9-]*)`)

func Parse(scriptContent string) []string {
	matches := flagRegex.FindAllStringSubmatch(scriptContent, -1)
	seen := make(map[string]bool)
	var flags []string
	for _, m := range matches {
		flag := strings.TrimPrefix(m[2], "--")
		if !seen[flag] {
			seen[flag] = true
			flags = append(flags, flag)
		}
	}
	sort.Strings(flags)
	return flags
}
