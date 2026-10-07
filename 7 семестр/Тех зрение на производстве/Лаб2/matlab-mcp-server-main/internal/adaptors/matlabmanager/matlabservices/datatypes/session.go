// Copyright 2025 The MathWorks, Inc.

package datatypes

type SessionID int

type LocalSessionDetails struct {
	MATLABRoot             string
	IsStartingDirectorySet bool
	StartingDirectory      string
	ShowMATLABDesktop      bool
}
