// Copyright 2025 The MathWorks, Inc.

package osfacade

import (
	"os"
	"time"
)

type FileInfo interface {
	Name() string
	Size() int64
	Mode() FileMode
	ModTime() time.Time
	IsDir() bool
	Sys() any
}

type FileInfoWrapper struct {
	os.FileInfo
}

func (fiw *FileInfoWrapper) Mode() FileMode {
	return FileModeWrapper{fiw.FileInfo.Mode()}
}

type FileMode interface {
	Perm() uint32
}

type FileModeWrapper struct {
	os.FileMode
}

// Perm wraps the FileMode perm method.
// It converts the output to a uint32 for convenience in testing.
func (fmw FileModeWrapper) Perm() uint32 {
	return uint32(fmw.FileMode.Perm())
}

// Stat wraps the os.Stat function.
func (*OsFacade) Stat(name string) (FileInfo, error) {
	info, err := os.Stat(name)
	return &FileInfoWrapper{info}, err
}

// File provides an interface for interacting with files.
type File interface {
	Write(b []byte) (int, error)
	Read(b []byte) (int, error)
	Close() error
	Name() string
	Fd() uintptr

	// Provide method for retreiving original file to facilitate passing to os.StartProcess
	Unwrap() *os.File
}

type FileWrapper struct {
	*os.File
}

// Unwrap returns the original file pointer so it can be passed to the Files list of os.ProcAttr
func (fw *FileWrapper) Unwrap() *os.File {
	return fw.File
}

// Open wraps the os.Open function to open a file for reading.
func (osw *OsFacade) Open(path string) (File, error) {
	file, err := os.Open(path) //nolint:gosec // Intentional os.Open usage in facade
	if err != nil {
		return nil, err
	}
	return &FileWrapper{file}, nil
}

// MkdirTemp wraps the os.MkdirTemp function to create a temp directory.
func (osw *OsFacade) MkdirTemp(dir string, pattern string) (string, error) {
	return os.MkdirTemp(dir, pattern)
}

// Mkdir wraps the os.Mkdir function to create a directory.
func (osw *OsFacade) Mkdir(name string, perm os.FileMode) error {
	return os.Mkdir(name, perm)
}

// MkdirAll wraps the os.MkdirAll function to create a directory.
func (osw *OsFacade) MkdirAll(name string, perm os.FileMode) error {
	return os.MkdirAll(name, perm)
}

// RemoveAll wraps the os.RemoveAll function to create a delete a directory and its children.
func (osw *OsFacade) RemoveAll(path string) error {
	return os.RemoveAll(path)
}

// ReadFile wraps the os.ReadFile function to read a file content.
func (osw *OsFacade) ReadFile(filePath string) ([]byte, error) {
	return os.ReadFile(filePath) //nolint:gosec // Intentional os.ReadFile usage in facade
}

// WriteFile wraps the os.WriteFile function to write content to a file.
func (osw *OsFacade) WriteFile(name string, data []byte, perm os.FileMode) error {
	return os.WriteFile(name, data, perm)
}

// UserHomeDir wraps the os.UserHomeDir function to get the user's home directory
func (osw *OsFacade) UserHomeDir() (string, error) {
	return os.UserHomeDir()
}

// Create wraps the os.Create function to create a file.
func (osw *OsFacade) Create(name string) (File, error) {
	file, err := os.Create(name) //nolint:gosec // Intentional os.Create usage in facade
	if err != nil {
		return nil, err
	}

	return &FileWrapper{file}, nil
}

// CreateTemp wraps the os.CreateTemp function to create a file with a unique suffix.
func (osw *OsFacade) CreateTemp(dir string, pattern string) (File, error) {
	file, err := os.CreateTemp(dir, pattern)
	if err != nil {
		return nil, err
	}

	return &FileWrapper{file}, nil
}
