// Copyright 2025 The MathWorks, Inc.

package iofacade

import "io"

type IoFacade struct {
}

func New() *IoFacade {
	return &IoFacade{}
}

func (iof *IoFacade) ReadAll(r io.Reader) ([]byte, error) {
	return io.ReadAll(r)
}
