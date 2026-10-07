// Copyright 2025 The MathWorks, Inc.

package filefacade

import "path/filepath"

type FileFacade struct {
}

func New() *FileFacade {
	return &FileFacade{}
}

// EvalSymlinks wraps the filepath.EvalSymlinks function to resolve any symbolic links in the given path.
func (ff *FileFacade) EvalSymlinks(path string) (string, error) {
	return filepath.EvalSymlinks(path)
}
