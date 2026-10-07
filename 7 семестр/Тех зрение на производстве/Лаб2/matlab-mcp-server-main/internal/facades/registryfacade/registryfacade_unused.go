// Copyright 2026 The MathWorks, Inc.

//go:build !windows

package registryfacade

// This is a dummy impl so that mockery can generate the mock

type RegistryKey interface {
	GetStringValue(name string) (string, uint32, error)
	Close() error
}

type RegistryFacade struct{}

func New() *RegistryFacade {
	return &RegistryFacade{}
}

// OpenKey wraps the registry.OpenKey function to open a registry key.
func (rf *RegistryFacade) OpenKey(k uintptr, path string, access uint32) (RegistryKey, error) {
	return nil, nil
}
