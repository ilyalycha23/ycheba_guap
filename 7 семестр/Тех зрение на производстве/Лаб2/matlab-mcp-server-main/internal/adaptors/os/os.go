// Copyright 2026 The MathWorks, Inc.

package os

import (
	"github.com/matlab/matlab-mcp-server/internal/facades/osfacade"
	"github.com/matlab/matlab-mcp-server/internal/facades/registryfacade"
)

type VersionOSLayer interface {
	Command(name string, arg ...string) osfacade.Cmd
	Open(path string) (osfacade.File, error)
}

type RegistryLayer interface {
	OpenKey(k uintptr, path string, access uint32) (registryfacade.RegistryKey, error)
}

type OS struct {
	osLayer       VersionOSLayer
	registryLayer RegistryLayer
}

func New(
	osLayer VersionOSLayer,
	registryLayer RegistryLayer,
) OS {
	return OS{
		osLayer:       osLayer,
		registryLayer: registryLayer,
	}
}
