// Copyright 2026 The MathWorks, Inc.

package matlabstring

import "strings"

// EscapeSingleQuotes escapes single quotes in a string for use inside
// a MATLAB single-quoted string literal by doubling each occurrence.
func EscapeSingleQuotes(s string) string {
	return strings.ReplaceAll(s, "'", "''")
}
