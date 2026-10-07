// Copyright 2025-2026 The MathWorks, Inc.

package listavailablematlabs

const (
	name        = "list_available_matlabs"
	title       = "List Available MATLABs"
	description = "List the installed MATLAB versions on the host and their root directories."
)

type Args struct{}

type ReturnArgs struct {
	AvailableMATLABs []EnvironmentInfo `json:"available_matlabs" jsonschema:"A list of available MATLAB versions on the host."`
}

type EnvironmentInfo struct {
	Version    string `json:"version"     jsonschema:"The MATLAB version."`
	MATLABRoot string `json:"matlab_root" jsonschema:"The MATLAB installation root folder."`
}
