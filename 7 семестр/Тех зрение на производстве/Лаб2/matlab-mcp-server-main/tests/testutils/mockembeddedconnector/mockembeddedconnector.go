// Copyright 2026 The MathWorks, Inc.

package mockembeddedconnector

import (
	"encoding/json"
	"encoding/pem"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/matlabmanager/matlabsessionclient/embeddedconnector"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

type Server struct {
	httpServer        *httptest.Server
	connectionDetails embeddedconnector.ConnectionDetails
}

func New(t *testing.T, evalHandler, stateHandler http.HandlerFunc) *Server {
	t.Helper()

	const apiKey = "test-api-key"

	mux := http.NewServeMux()

	if evalHandler != nil {
		mux.HandleFunc("/messageservice/json/secure", requireConnectorRequest(t, apiKey, evalHandler))
	}
	if stateHandler != nil {
		mux.HandleFunc("/messageservice/json/state", requireConnectorRequest(t, apiKey, stateHandler))
	}

	server := httptest.NewTLSServer(mux)

	addressParts := strings.Split(server.Listener.Addr().String(), ":")
	certPEM := pem.EncodeToMemory(&pem.Block{
		Type:  "CERTIFICATE",
		Bytes: server.Certificate().Raw,
	})

	return &Server{
		httpServer: server,
		connectionDetails: embeddedconnector.ConnectionDetails{
			Host:           addressParts[0],
			Port:           addressParts[1],
			APIKey:         apiKey,
			CertificatePEM: certPEM,
		},
	}
}

func (s *Server) ConnectionDetails() embeddedconnector.ConnectionDetails {
	return s.connectionDetails
}

func (s *Server) Stop() {
	s.httpServer.Close()
}

func requireConnectorRequest(t assert.TestingT, apiKey string, next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		assert.Equal(t, http.MethodPost, r.Method)
		assert.Equal(t, "application/json", r.Header.Get("Content-Type"))
		assert.Equal(t, apiKey, r.Header.Get("mwapikey"))
		next(w, r)
	}
}

func RespondWithJSON(t *testing.T, w http.ResponseWriter, payload any) {
	t.Helper()

	w.Header().Set("Content-Type", "application/json")
	require.NoError(t, json.NewEncoder(w).Encode(payload))
}

func ReadConnectorRequest(t *testing.T, r *http.Request) embeddedconnector.ConnectorPayload {
	t.Helper()

	body, err := io.ReadAll(r.Body)
	require.NoError(t, err)
	var payload embeddedconnector.ConnectorPayload
	require.NoError(t, json.Unmarshal(body, &payload))
	return payload
}
