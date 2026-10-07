// Copyright 2025 The MathWorks, Inc.

package datatypes

type MatlabVersionInfo struct {
	ReleaseFamily string
	ReleasePhase  string
	UpdateLevel   int
}

type MatlabInfo struct {
	Version  MatlabVersionInfo
	Location string
}

type ListMatlabInfo struct {
	MatlabInfo []MatlabInfo
}
