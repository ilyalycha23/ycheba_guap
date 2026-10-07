// Copyright 2025-2026 The MathWorks, Inc.

package mcpserver

import (
	"fmt"
	"regexp"
	"sort"
	"strings"
)

var helpFlagRegex = regexp.MustCompile(`^\s+--(\S+)`)

func ParseVersion(versionOutput string) (string, error) {
	parts := strings.Fields(strings.TrimSpace(versionOutput))
	if len(parts) == 0 {
		return "", fmt.Errorf("empty version output")
	}
	return parts[len(parts)-1], nil
}

func ParseHelpFlags(helpOutput string) []string {
	var flags []string
	inUsage := false
	for line := range strings.SplitSeq(helpOutput, "\n") {
		line = strings.TrimRight(line, "\r")
		if strings.HasPrefix(line, "Usage:") {
			inUsage = true
			continue
		}
		if !inUsage {
			continue
		}
		if m := helpFlagRegex.FindStringSubmatch(line); m != nil {
			flags = append(flags, m[1])
		}
	}
	sort.Strings(flags)
	return flags
}
