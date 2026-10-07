// Copyright 2025 The MathWorks, Inc.
//go:build windows

package winenvironmentbuilder

import (
	"fmt"
	"sort"
	"strings"

	"golang.org/x/sys/windows"
)

type envEntry struct {
	upperName string
	entry     string
}

// Build creates a UTF-16 environment block suitable for CreateProcess.
//   - Each entry is "name=value" NUL-terminated
//   - The block ends with an extra NUL
//   - Entries are sorted case-insensitively by name (Windows requirement for Unicode blocks)
//   - Duplicate names are resolved by keeping the last occurrence
//   - Special Windows drive variables (e.g., "=C:=C:\path") are preserved
//
// Returns a []uint16 slice (environmentBlock). Use PointerToFirstElement() to get the *uint16 for CreateProcess.
// Returns nil for empty input.
//
// Note: Case folding uses Go's strings.ToUpper which follows Unicode rules. Windows uses
// locale-specific case folding which may differ for some non-ASCII characters. This is
// acceptable for typical environment variables which use ASCII names.
func Build(env []string) (environmentBlock, error) {
	if len(env) == 0 {
		return nil, nil
	}

	deduped, err := deduplicateCaseInsensitive(env)
	if err != nil {
		return nil, err
	}

	sorted := sortEntriesByName(deduped)

	return encodeToUTF16Block(sorted), nil
}

// BlockPointer returns a pointer to the first element of the block,
// suitable for passing to windows.CreateProcess. Returns nil for empty/nil blocks.
type environmentBlock []uint16

func (b environmentBlock) PointerToFirstElement() *uint16 {
	if len(b) == 0 {
		return nil
	}
	return &b[0]
}

func deduplicateCaseInsensitive(env []string) ([]envEntry, error) {
	seen := make(map[string]int, len(env)) // upperName -> index in entries
	entries := make([]envEntry, 0, len(env))

	for _, e := range env {
		if err := validateNoNUL(e); err != nil {
			return nil, err
		}

		name, value, ok := parseEntry(e)
		if !ok {
			return nil, fmt.Errorf("invalid environment entry (expected name=value): %q", e)
		}

		upperName := strings.ToUpper(name)
		entry := envEntry{upperName: upperName, entry: name + "=" + value}

		if idx, exists := seen[upperName]; exists {
			entries[idx] = entry // replace duplicate
		} else {
			seen[upperName] = len(entries)
			entries = append(entries, entry)
		}
	}
	return entries, nil
}

func validateNoNUL(entry string) error {
	if strings.IndexByte(entry, 0) >= 0 {
		return fmt.Errorf("environment entry contains NUL: %q", entry)
	}
	return nil
}

func sortEntriesByName(entries []envEntry) []string {
	sort.Slice(entries, func(i, j int) bool {
		return entries[i].upperName < entries[j].upperName
	})

	sorted := make([]string, len(entries))
	for i, e := range entries {
		sorted[i] = e.entry
	}
	return sorted
}

func encodeToUTF16Block(entries []string) []uint16 {
	var block []uint16
	for _, entry := range entries {
		utf16Entry, _ := windows.UTF16FromString(entry) // includes trailing NUL
		block = append(block, utf16Entry...)
	}
	block = append(block, 0) // final NUL terminator
	return block
}

// parseEntry parses an environment entry in the form "name=value".
// For Windows hidden variables starting with "=", the name includes the leading "="
// and extends to the second "=" (e.g., "=C:=C:\path" -> name="=C:", value="C:\path").
func parseEntry(entry string) (name, value string, ok bool) {
	// Handle Windows hidden environment variables that start with "="
	if len(entry) >= 2 && entry[0] == '=' {
		// Find the second "=" which separates name from value
		idx := strings.IndexByte(entry[1:], '=')
		if idx > 0 {
			return entry[:idx+1], entry[idx+2:], true
		}
		return "", "", false
	}

	name, value, ok = strings.Cut(entry, "=")
	if !ok || name == "" {
		return "", "", false
	}
	return name, value, true
}
