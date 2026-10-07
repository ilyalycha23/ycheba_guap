// Copyright 2026 The MathWorks, Inc.

package mockembeddedconnector_test

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/matlabmanager/matlabsessionclient/embeddedconnector"
	"github.com/matlab/matlab-mcp-server/tests/testutils/mockembeddedconnector"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestNew_NilEvalHandler_Returns404OnEvalPath(t *testing.T) {
	// Arrange
	server := mockembeddedconnector.New(t, nil, nil)
	defer server.Stop()

	// Act
	resp, err := server.HTTPClient().Post(server.URL()+"/messageservice/json/secure", "application/json", nil)
	require.NoError(t, err)
	defer require.NoError(t, resp.Body.Close())

	// Assert
	assert.Equal(t, http.StatusNotFound, resp.StatusCode)
}

func TestNew_NilStateHandler_Returns404OnStatePath(t *testing.T) {
	// Arrange
	server := mockembeddedconnector.New(t, nil, nil)
	defer server.Stop()

	// Act
	resp, err := server.HTTPClient().Post(server.URL()+"/messageservice/json/state", "application/json", nil)
	require.NoError(t, err)
	defer require.NoError(t, resp.Body.Close())

	// Assert
	assert.Equal(t, http.StatusNotFound, resp.StatusCode)
}

func TestNew_UnsupportedPath_Returns404(t *testing.T) {
	// Arrange
	evalHandler := func(w http.ResponseWriter, r *http.Request) {}
	stateHandler := func(w http.ResponseWriter, r *http.Request) {}

	server := mockembeddedconnector.New(t, evalHandler, stateHandler)
	defer server.Stop()

	// Act
	resp, err := server.HTTPClient().Post(server.URL()+"/some/unsupported/path", "application/json", nil)
	require.NoError(t, err)
	defer require.NoError(t, resp.Body.Close())

	// Assert
	assert.Equal(t, http.StatusNotFound, resp.StatusCode)
}

func TestNew_BothHandlersRegistered_RoutesToEvalHandler(t *testing.T) {
	// Arrange
	evalCalled := false
	stateCalled := false

	server := mockembeddedconnector.New(t,
		func(w http.ResponseWriter, r *http.Request) {
			evalCalled = true
		},
		func(w http.ResponseWriter, r *http.Request) {
			stateCalled = true
		},
	)
	defer server.Stop()

	details := server.ConnectionDetails()
	req, err := http.NewRequest(http.MethodPost, server.URL()+"/messageservice/json/secure", nil)
	require.NoError(t, err)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("mwapikey", details.APIKey)

	// Act
	resp, err := server.HTTPClient().Do(req)
	require.NoError(t, err)
	defer require.NoError(t, resp.Body.Close())

	// Assert
	assert.True(t, evalCalled)
	assert.False(t, stateCalled)
}

func TestNew_BothHandlersRegistered_RoutesToStateHandler(t *testing.T) {
	// Arrange
	evalCalled := false
	stateCalled := false

	server := mockembeddedconnector.New(t,
		func(w http.ResponseWriter, r *http.Request) {
			evalCalled = true
		},
		func(w http.ResponseWriter, r *http.Request) {
			stateCalled = true
		},
	)
	defer server.Stop()

	details := server.ConnectionDetails()
	req, err := http.NewRequest(http.MethodPost, server.URL()+"/messageservice/json/state", nil)
	require.NoError(t, err)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("mwapikey", details.APIKey)

	// Act
	resp, err := server.HTTPClient().Do(req)
	require.NoError(t, err)
	defer require.NoError(t, resp.Body.Close())

	// Assert
	assert.False(t, evalCalled)
	assert.True(t, stateCalled)
}

func TestRespondWithJSON_SetsContentTypeAndEncodesPayload(t *testing.T) {
	// Arrange
	expectedPayload := embeddedconnector.ConnectorPayload{
		Messages: embeddedconnector.ConnectorMessage{
			EvalResponse: []embeddedconnector.EvalResponseMessage{
				{
					IsError:     false,
					ResponseStr: "hello",
				},
			},
		},
	}

	recorder := httptest.NewRecorder()

	// Act
	mockembeddedconnector.RespondWithJSON(t, recorder, expectedPayload)

	// Assert
	result := recorder.Result()
	defer require.NoError(t, result.Body.Close())

	assert.Equal(t, "application/json", result.Header.Get("Content-Type"))

	var actual embeddedconnector.ConnectorPayload
	require.NoError(t, json.NewDecoder(result.Body).Decode(&actual))
	assert.Equal(t, expectedPayload, actual)
}

func TestRequireConnectorRequest_WrongMethod_FailsTest(t *testing.T) {
	// Arrange
	recorder := &mockembeddedconnector.FailRecorder{}
	handler := mockembeddedconnector.RequireConnectorRequest(recorder, "test-key",
		func(w http.ResponseWriter, r *http.Request) {},
	)

	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("mwapikey", "test-key")
	resp := httptest.NewRecorder()

	// Act
	handler.ServeHTTP(resp, req)

	// Assert
	assert.True(t, recorder.DidFail)
}

func TestRequireConnectorRequest_MissingContentType_FailsTest(t *testing.T) {
	// Arrange
	recorder := &mockembeddedconnector.FailRecorder{}
	handler := mockembeddedconnector.RequireConnectorRequest(recorder, "test-key",
		func(w http.ResponseWriter, r *http.Request) {},
	)

	req := httptest.NewRequest(http.MethodPost, "/test", nil)
	req.Header.Set("mwapikey", "test-key")
	resp := httptest.NewRecorder()

	// Act
	handler.ServeHTTP(resp, req)

	// Assert
	assert.True(t, recorder.DidFail)
}

func TestRequireConnectorRequest_WrongContentType_FailsTest(t *testing.T) {
	// Arrange
	recorder := &mockembeddedconnector.FailRecorder{}
	handler := mockembeddedconnector.RequireConnectorRequest(recorder, "test-key",
		func(w http.ResponseWriter, r *http.Request) {},
	)

	req := httptest.NewRequest(http.MethodPost, "/test", nil)
	req.Header.Set("Content-Type", "text/plain")
	req.Header.Set("mwapikey", "test-key")
	resp := httptest.NewRecorder()

	// Act
	handler.ServeHTTP(resp, req)

	// Assert
	assert.True(t, recorder.DidFail)
}

func TestRequireConnectorRequest_MissingAPIKey_FailsTest(t *testing.T) {
	// Arrange
	recorder := &mockembeddedconnector.FailRecorder{}
	handler := mockembeddedconnector.RequireConnectorRequest(recorder, "test-key",
		func(w http.ResponseWriter, r *http.Request) {},
	)

	req := httptest.NewRequest(http.MethodPost, "/test", nil)
	req.Header.Set("Content-Type", "application/json")
	resp := httptest.NewRecorder()

	// Act
	handler.ServeHTTP(resp, req)

	// Assert
	assert.True(t, recorder.DidFail)
}

func TestRequireConnectorRequest_WrongAPIKey_FailsTest(t *testing.T) {
	// Arrange
	recorder := &mockembeddedconnector.FailRecorder{}
	handler := mockembeddedconnector.RequireConnectorRequest(recorder, "test-key",
		func(w http.ResponseWriter, r *http.Request) {},
	)

	req := httptest.NewRequest(http.MethodPost, "/test", nil)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("mwapikey", "wrong-key")
	resp := httptest.NewRecorder()

	// Act
	handler.ServeHTTP(resp, req)

	// Assert
	assert.True(t, recorder.DidFail)
}

func TestReadConnectorRequest_DeserializesBody(t *testing.T) {
	// Arrange
	expectedPayload := embeddedconnector.ConnectorPayload{
		Messages: embeddedconnector.ConnectorMessage{
			Eval: []embeddedconnector.EvalMessage{
				{Code: "disp('test')"},
			},
		},
	}

	body, err := json.Marshal(expectedPayload)
	require.NoError(t, err)

	request := httptest.NewRequest(http.MethodPost, "/messageservice/json/secure", bytes.NewReader(body))
	request.Header.Set("Content-Type", "application/json")

	// Act
	actual := mockembeddedconnector.ReadConnectorRequest(t, request)

	// Assert
	assert.Equal(t, expectedPayload, actual)
}
