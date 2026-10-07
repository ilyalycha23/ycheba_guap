// Copyright 2025-2026 The MathWorks, Inc.

package osfacade

import (
	"io"
	"os"
	"path/filepath"
	"runtime"
)

// Environ wraps the os.Environ function to retrieve the environment variables.
func (osw *OsFacade) Environ() []string {
	return os.Environ()
}

// Args wraps the os.Args to get process arguments.
func (osw *OsFacade) Args() []string {
	return os.Args
}

// Getenv wraps the os.Getenv function to retrieve the value of the environment variable named by the key.
func (osw *OsFacade) Getenv(key string) string {
	return os.Getenv(key)
}

// LookupEnv wraps the os.LookupEnv function to retrieve the value of the environment variable named by the key.
func (osw *OsFacade) LookupEnv(key string) (string, bool) {
	return os.LookupEnv(key)
}

// Stdin wraps the os.Stdin function to retrieve the process stdin.
func (osw *OsFacade) Stdin() io.Reader {
	return os.Stdin
}

// Stdout wraps the os.Stdout function to retrieve the process stdout.
func (osw *OsFacade) Stdout() io.Writer {
	return os.Stdout
}

// Stderr wraps the os.Stderr function to retrieve the process stderr.
func (osw *OsFacade) Stderr() io.Writer {
	return os.Stderr
}

// GOOS wraps the runtime.GOOS function to retrieve the OS.
func (osw *OsFacade) GOOS() string {
	return runtime.GOOS
}

// IsAbs wraps filepath.IsAbs to check whether a path is absolute.
func (osw *OsFacade) IsAbs(path string) bool {
	return filepath.IsAbs(path)
}
