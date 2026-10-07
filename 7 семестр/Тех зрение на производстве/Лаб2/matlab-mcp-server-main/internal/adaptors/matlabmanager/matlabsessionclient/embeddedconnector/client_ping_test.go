// Copyright 2025-2026 The MathWorks, Inc.

package embeddedconnector_test

import (
	"bytes"
	"context"
	"encoding/json"
	"io"
	"net/http"
	"strings"
	"testing"
	"time"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/matlabmanager/matlabsessionclient/embeddedconnector"
	"github.com/matlab/matlab-mcp-server/internal/testutils"
	httpclientmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/http/client"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

func TestClient_Ping_HappyPath(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	responsePayload := embeddedconnector.ConnectorPayload{
		Messages: embeddedconnector.ConnectorMessage{
			PingResponse: []embeddedconnector.PingResponseMessage{
				{MessageFaults: []json.RawMessage{}},
			},
		},
	}
	responseBody, _ := json.Marshal(responsePayload)

	mockHttpClient.EXPECT().
		Do(mock.MatchedBy(func(req *http.Request) bool {
			payload, ok := parseConnectorRequest(req)
			if !ok {
				return false
			}
			return len(payload.Messages.Ping) == 1
		})).
		Return(&http.Response{
			StatusCode: http.StatusOK,
			Body:       io.NopCloser(bytes.NewReader(responseBody)),
		}, nil).
		Once()

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)
	client.SetPingRetry(10 * time.Millisecond)
	client.SetPingTimeout(100 * time.Millisecond)

	// Act
	response := client.Ping(t.Context(), mockLogger)

	// Assert
	assert.True(t, response.IsAlive)
}

func TestClient_Ping_HTTPError(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	mockHttpClient.EXPECT().
		Do(mock.MatchedBy(validateConnectorRequest)).
		Return(&http.Response{
			StatusCode: http.StatusInternalServerError,
			Status:     "500 Internal Server Error",
			Body:       io.NopCloser(bytes.NewReader([]byte{})),
		}, nil)

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)
	client.SetPingRetry(10 * time.Millisecond)
	client.SetPingTimeout(40 * time.Millisecond)

	// Act
	response := client.Ping(t.Context(), mockLogger)

	// Assert
	assert.False(t, response.IsAlive)
}

func TestClient_Ping_MATLABNotAvailable(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	fault := json.RawMessage(`{"message":"MATLAB is not available","faultCode":"MATLAB.PingError"}`)
	responsePayload := embeddedconnector.ConnectorPayload{
		Messages: embeddedconnector.ConnectorMessage{
			PingResponse: []embeddedconnector.PingResponseMessage{
				{MessageFaults: []json.RawMessage{fault}},
			},
		},
	}
	responseBody, _ := json.Marshal(responsePayload)

	mockHttpClient.EXPECT().
		Do(mock.MatchedBy(validateConnectorRequest)).
		Return(&http.Response{
			StatusCode: http.StatusOK,
			Body:       io.NopCloser(bytes.NewReader(responseBody)),
		}, nil)

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)
	client.SetPingRetry(10 * time.Millisecond)
	client.SetPingTimeout(40 * time.Millisecond)

	// Act
	response := client.Ping(t.Context(), mockLogger)

	// Assert
	assert.False(t, response.IsAlive)
}

func TestClient_Ping_NoResponseMessages(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	responsePayload := embeddedconnector.ConnectorPayload{
		Messages: embeddedconnector.ConnectorMessage{
			PingResponse: []embeddedconnector.PingResponseMessage{},
		},
	}
	responseBody, _ := json.Marshal(responsePayload)

	mockHttpClient.EXPECT().
		Do(mock.MatchedBy(validateConnectorRequest)).
		Return(&http.Response{
			StatusCode: http.StatusOK,
			Body:       io.NopCloser(bytes.NewReader(responseBody)),
		}, nil)

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)
	client.SetPingRetry(10 * time.Millisecond)
	client.SetPingTimeout(40 * time.Millisecond)

	// Act
	response := client.Ping(t.Context(), mockLogger)

	// Assert
	assert.False(t, response.IsAlive)
}

func TestClient_Ping_InvalidJSONResponse(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	mockHttpClient.EXPECT().
		Do(mock.MatchedBy(validateConnectorRequest)).
		Return(&http.Response{
			StatusCode: http.StatusOK,
			Body:       io.NopCloser(bytes.NewReader([]byte("invalid json"))),
		}, nil)

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)
	client.SetPingRetry(10 * time.Millisecond)
	client.SetPingTimeout(40 * time.Millisecond)

	// Act
	response := client.Ping(t.Context(), mockLogger)

	// Assert
	assert.False(t, response.IsAlive)
}

func TestClient_Ping_Retries(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	okResponse := &http.Response{
		StatusCode: http.StatusOK,
		Body:       io.NopCloser(strings.NewReader(`{"messages":{"pingResponse":[{}]}}`)),
	}

	mockHttpClient.EXPECT().
		Do(mock.MatchedBy(validateConnectorRequest)).
		Return(nil, assert.AnError).
		Once()

	mockHttpClient.EXPECT().
		Do(mock.MatchedBy(validateConnectorRequest)).
		Return(okResponse, nil).
		Once()

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)
	client.SetPingRetry(10 * time.Millisecond)
	client.SetPingTimeout(100 * time.Millisecond)

	ctx := t.Context()

	// Act
	response := client.Ping(ctx, mockLogger)

	// Assert
	assert.True(t, response.IsAlive)
}

func TestClient_Ping_Timeout(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	mockHttpClient.EXPECT().
		Do(mock.MatchedBy(validateConnectorRequest)).
		Return(nil, assert.AnError)

	pingTimeout := 100 * time.Millisecond
	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)
	client.SetPingRetry(10 * time.Millisecond)
	client.SetPingTimeout(pingTimeout)

	ctx := t.Context()

	// Act
	start := time.Now()
	response := client.Ping(ctx, mockLogger)
	duration := time.Since(start)

	// Assert
	assert.False(t, response.IsAlive, "Should return not alive after timeout")
	assert.GreaterOrEqual(t, duration, pingTimeout, "Should have waited for at least the timeout duration")
}

func TestClient_Ping_ContextPropagation(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	type contextKeyType string
	const contextKey contextKeyType = "uniqueKey"
	const contextKeyValue = "uniqueValue"

	expectedContext := context.WithValue(t.Context(), contextKey, contextKeyValue)
	expectedResponse := &http.Response{
		StatusCode: http.StatusOK,
		Body:       io.NopCloser(strings.NewReader(`{"messages":{"pingResponse":[{}]}}`)),
	}

	mockHttpClient.EXPECT().
		Do(mock.MatchedBy(func(request *http.Request) bool {
			return request.Context().Value(contextKey) == contextKeyValue
		})).
		Return(expectedResponse, nil).
		Once()

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)
	client.SetPingRetry(10 * time.Millisecond)
	client.SetPingTimeout(100 * time.Millisecond)

	// Act
	response := client.Ping(expectedContext, mockLogger)

	// Assert
	assert.True(t, response.IsAlive)
}
