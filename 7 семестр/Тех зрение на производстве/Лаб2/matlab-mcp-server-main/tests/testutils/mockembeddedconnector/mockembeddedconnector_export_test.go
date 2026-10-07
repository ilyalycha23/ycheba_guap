// Copyright 2026 The MathWorks, Inc.

package mockembeddedconnector

import (
	"net/http"

	"github.com/stretchr/testify/assert"
)

func (s *Server) HTTPClient() *http.Client {
	return s.httpServer.Client()
}

func (s *Server) URL() string {
	return s.httpServer.URL
}

func RequireConnectorRequest(t assert.TestingT, apiKey string, next http.HandlerFunc) http.HandlerFunc {
	return requireConnectorRequest(t, apiKey, next)
}

type FailRecorder struct {
	DidFail bool
}

func (r *FailRecorder) Errorf(format string, args ...any) {
	r.DidFail = true
}
