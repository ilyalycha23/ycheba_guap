// Copyright 2025 The MathWorks, Inc.

package stopmatlabsession

const (
	name        = "stop_matlab_session"
	title       = "Stop MATLAB Session"
	description = "Stops an existing MATLAB session, given its session ID (`session_id`)."
)

type Args struct {
	SessionID int `json:"session_id" jsonschema:"The ID of the MATLAB session to stop."`
}

type ReturnArgs struct {
	ResponseText string `json:"response_text" jsonschema:"A message indicating the result of the operation."`
}

const (
	responseTextIfMATLABSessionStoppedSuccessfully = "MATLAB session stopped successfully."
)
