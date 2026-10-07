// Copyright 2025 The MathWorks, Inc.
//go:build windows

package winenvironmentbuilder

// EnvironmentBlock is an alias for environmentBlock to allow testing.
type EnvironmentBlock = environmentBlock

// EncodeEntries encodes string entries to a UTF-16 block for test comparisons.
func EncodeEntries(entries []string) EnvironmentBlock {
	return encodeToUTF16Block(entries)
}
