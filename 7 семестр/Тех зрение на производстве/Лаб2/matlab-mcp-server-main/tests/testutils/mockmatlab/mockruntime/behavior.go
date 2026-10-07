// Copyright 2026 The MathWorks, Inc.

package mockruntime

import "strings"

func ShouldExitFromEvalCode(code string) bool {
	code = stripHotLinksPrefix(code)
	switch code {
	case "exit()", "exit", "quit", "quit()":
		return true
	default:
		return false
	}
}

func stripHotLinksPrefix(code string) string {
	return strings.TrimPrefix(code, "feature('HotLinks',0);")
}
