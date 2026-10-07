// Copyright 2026 The MathWorks, Inc.

//go:build windows

package os

import (
	"fmt"

	"golang.org/x/sys/windows/registry"
)

func (o OS) Version() (string, error) {
	key, err := o.registryLayer.OpenKey(uintptr(registry.LOCAL_MACHINE), `SOFTWARE\Microsoft\Windows NT\CurrentVersion`, registry.QUERY_VALUE)
	if err != nil {
		return "", err
	}
	defer func() { _ = key.Close() }()

	productName, _, err := key.GetStringValue("ProductName")
	if err != nil {
		return "", err
	}

	buildNumber, _, _ := key.GetStringValue("CurrentBuildNumber")

	if buildNumber != "" {
		return fmt.Sprintf("%s (Build %s)", productName, buildNumber), nil
	}
	return productName, nil
}
