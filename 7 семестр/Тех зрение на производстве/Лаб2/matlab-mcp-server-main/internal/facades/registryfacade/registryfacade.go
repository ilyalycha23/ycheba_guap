// Copyright 2026 The MathWorks, Inc.

//go:build windows

package registryfacade

import "golang.org/x/sys/windows/registry"

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
	key, err := registry.OpenKey(registry.Key(k), path, access)
	if err != nil {
		return nil, err
	}
	return &key, nil
}
