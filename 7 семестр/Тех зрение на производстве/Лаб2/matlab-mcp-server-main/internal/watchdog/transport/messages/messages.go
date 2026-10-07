// Copyright 2025 The MathWorks, Inc.

package messages

const (
	ProcessToKillPath = "/process"
	ShutdownPath      = "/shutdown"
)

type ProcessToKillRequest struct {
	PID int `json:"pid"`
}

type ProcessToKillResponse struct{}

type ShutdownRequest struct{}

type ShutdownResponse struct{}
