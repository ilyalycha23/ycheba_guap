// Copyright 2025-2026 The MathWorks, Inc.

package startmatlabsession

const (
	name        = "start_matlab_session"
	title       = "Start MATLAB Session"
	description = "Starts a new MATLAB session for the provided MATLAB root (`matlab_root`) and returns a session ID (`session_id`)."
)

type Args struct {
	MATLABRoot string `json:"matlab_root" jsonschema:"MATLAB root folder for session."`
}

type ReturnArgs struct {
	ResponseText string `json:"response_text"  jsonschema:"A message indicating the result of the operation."`
	SessionID    int    `json:"session_id"     jsonschema:"The ID of the newly started MATLAB session."`
	VerOutput    string `json:"ver_output"     jsonschema:"Output of the ver command, listing installed MATLAB Toolboxes."`
	AddOnsOutput string `json:"add_ons_output" jsonschema:"List of installed Add-Ons, other than MATLAB Toolboxes (e.g. Support Packages, community Add-Ons)."`
}

const (
	responseTextIfMATLABSessionStartedSuccesfully = "MATLAB session started successfully."
)
