// Copyright 2026 The MathWorks, Inc.

package buildinfo

import "runtime/debug"

type OSLayer interface {
	ReadBuildInfo() (info *debug.BuildInfo, ok bool)
}

type BuildInfo struct {
	osLayer OSLayer
}

func New(
	osLayer OSLayer,
) *BuildInfo {
	return &BuildInfo{
		osLayer: osLayer,
	}
}

func (d *BuildInfo) Version() string {
	_, version := d.version()
	return version
}

func (d *BuildInfo) FullVersion() string {
	fullVersion, _ := d.version()
	return fullVersion
}

func (d *BuildInfo) version() (string, string) {
	buildInfo, ok := d.osLayer.ReadBuildInfo()
	if !ok {
		return "(unknown)", "(unknown)"
	}

	version := buildInfo.Main.Version
	if version == "" {
		version = "(devel)"
	}

	return buildInfo.Main.Path + " " + version, version
}
