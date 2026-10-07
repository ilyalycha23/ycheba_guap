// Copyright 2025-2026 The MathWorks, Inc.

package embeddedconnector_test

import (
	"bytes"
	"context"
	"encoding/json"
	"io"
	"net/http"
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/matlabmanager/matlabsessionclient/embeddedconnector"
	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/testutils"
	httpclientmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/http/client"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
	"github.com/stretchr/testify/require"
)

func TestClient_FEval_HappyPath(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	expectedFunction := "size"
	expectedArguments := []string{"a"}
	expectedNumOutputs := 2
	expectedResults := []interface{}{"result1", "result2"}

	responsePayload := embeddedconnector.ConnectorPayload{
		Messages: embeddedconnector.ConnectorMessage{
			FevalResponse: []embeddedconnector.FevalResponseMessage{
				{
					IsError: false,
					Results: expectedResults,
				},
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
			if len(payload.Messages.FEval) != 1 {
				return false
			}
			feval := payload.Messages.FEval[0]
			return feval.Function == expectedFunction &&
				len(feval.Arguments) == len(expectedArguments) &&
				feval.Nargout == expectedNumOutputs
		})).
		Return(&http.Response{
			StatusCode: http.StatusOK,
			Body:       io.NopCloser(bytes.NewReader(responseBody)),
		}, nil).
		Once()

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)

	// Act
	response, err := client.FEval(t.Context(), mockLogger, entities.FEvalRequest{
		Function:   expectedFunction,
		Arguments:  expectedArguments,
		NumOutputs: expectedNumOutputs,
	})

	// Assert
	require.NoError(t, err)
	assert.Equal(t, expectedResults, response.Outputs)
}

func TestClient_FEval_MultipleOutputs(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	expectedFunction := "size"
	expectedArguments := []string{"a"}
	expectedNumOutputs := 2
	expectedResults := []interface{}{"2", "3"}

	responsePayload := embeddedconnector.ConnectorPayload{
		Messages: embeddedconnector.ConnectorMessage{
			FevalResponse: []embeddedconnector.FevalResponseMessage{
				{
					IsError: false,
					Results: expectedResults,
				},
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
			if len(payload.Messages.FEval) != 1 {
				return false
			}
			feval := payload.Messages.FEval[0]
			return feval.Function == expectedFunction &&
				len(feval.Arguments) == len(expectedArguments) &&
				feval.Nargout == expectedNumOutputs
		})).
		Return(&http.Response{
			StatusCode: http.StatusOK,
			Body:       io.NopCloser(bytes.NewReader(responseBody)),
		}, nil).
		Once()

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)

	// Act
	response, err := client.FEval(t.Context(), mockLogger, entities.FEvalRequest{
		Function:   expectedFunction,
		Arguments:  expectedArguments,
		NumOutputs: expectedNumOutputs,
	})

	// Assert
	require.NoError(t, err)
	assert.Equal(t, expectedResults, response.Outputs)
}

func TestClient_FEval_NoArguments(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	expectedFunction := "rand"
	expectedNumOutputs := 1
	expectedResults := []interface{}{"0.8147"}

	responsePayload := embeddedconnector.ConnectorPayload{
		Messages: embeddedconnector.ConnectorMessage{
			FevalResponse: []embeddedconnector.FevalResponseMessage{
				{
					IsError: false,
					Results: expectedResults,
				},
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
			if len(payload.Messages.FEval) != 1 {
				return false
			}
			feval := payload.Messages.FEval[0]
			return feval.Function == expectedFunction &&
				len(feval.Arguments) == 0 &&
				feval.Nargout == expectedNumOutputs
		})).
		Return(&http.Response{
			StatusCode: http.StatusOK,
			Body:       io.NopCloser(bytes.NewReader(responseBody)),
		}, nil).
		Once()

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)

	// Act
	response, err := client.FEval(t.Context(), mockLogger, entities.FEvalRequest{
		Function:   expectedFunction,
		Arguments:  []string{},
		NumOutputs: expectedNumOutputs,
	})

	// Assert
	require.NoError(t, err)
	assert.Equal(t, expectedResults, response.Outputs)
}

func TestClient_FEval_HTTPError(t *testing.T) {
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
		}, nil).
		Once()

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)

	// Act
	response, err := client.FEval(t.Context(), mockLogger, entities.FEvalRequest{Function: "sum"})

	// Assert
	require.Error(t, err)
	assert.Contains(t, err.Error(), "500")
	assert.Empty(t, response)
}

func TestClient_FEval_MATLABError(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	expectedErrorMessage := "Undefined function 'invalid_function'"

	faultMessage := embeddedconnector.Fault{Message: expectedErrorMessage}
	faultBytes, _ := json.Marshal(faultMessage)

	responsePayload := embeddedconnector.ConnectorPayload{
		Messages: embeddedconnector.ConnectorMessage{
			FevalResponse: []embeddedconnector.FevalResponseMessage{
				{
					IsError:       true,
					MessageFaults: []json.RawMessage{faultBytes},
				},
			},
		},
	}
	responseBody, _ := json.Marshal(responsePayload)

	mockHttpClient.EXPECT().
		Do(mock.MatchedBy(validateConnectorRequest)).
		Return(&http.Response{
			StatusCode: http.StatusOK,
			Body:       io.NopCloser(bytes.NewReader(responseBody)),
		}, nil).
		Once()

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)

	// Act
	response, err := client.FEval(t.Context(), mockLogger, entities.FEvalRequest{Function: "invalid_function"})

	// Assert
	require.Error(t, err)
	assert.Contains(t, err.Error(), expectedErrorMessage)
	assert.Nil(t, response.Outputs)
}

func TestClient_FEval_MATLABErrorWithMultipleFaults(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	expectedErrorMessage1 := "First error message"
	expectedErrorMessage2 := "Second error message"

	fault1Bytes, _ := json.Marshal(embeddedconnector.Fault{Message: expectedErrorMessage1})
	fault2Bytes, _ := json.Marshal(embeddedconnector.Fault{Message: expectedErrorMessage2})

	responsePayload := embeddedconnector.ConnectorPayload{
		Messages: embeddedconnector.ConnectorMessage{
			FevalResponse: []embeddedconnector.FevalResponseMessage{
				{
					IsError:       true,
					MessageFaults: []json.RawMessage{fault1Bytes, fault2Bytes},
				},
			},
		},
	}
	responseBody, _ := json.Marshal(responsePayload)

	mockHttpClient.EXPECT().
		Do(mock.MatchedBy(validateConnectorRequest)).
		Return(&http.Response{
			StatusCode: http.StatusOK,
			Body:       io.NopCloser(bytes.NewReader(responseBody)),
		}, nil).
		Once()

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)

	// Act
	response, err := client.FEval(t.Context(), mockLogger, entities.FEvalRequest{Function: "invalid_function"})

	// Assert
	require.Error(t, err)
	assert.Contains(t, err.Error(), expectedErrorMessage1)
	assert.Contains(t, err.Error(), expectedErrorMessage2)
	assert.Nil(t, response.Outputs)
}

func TestClient_FEval_MATLABErrorWithNoFaults(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	responsePayload := embeddedconnector.ConnectorPayload{
		Messages: embeddedconnector.ConnectorMessage{
			FevalResponse: []embeddedconnector.FevalResponseMessage{
				{
					IsError:       true,
					MessageFaults: []json.RawMessage{},
				},
			},
		},
	}
	responseBody, _ := json.Marshal(responsePayload)

	mockHttpClient.EXPECT().
		Do(mock.MatchedBy(validateConnectorRequest)).
		Return(&http.Response{
			StatusCode: http.StatusOK,
			Body:       io.NopCloser(bytes.NewReader(responseBody)),
		}, nil).
		Once()

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)

	// Act
	response, err := client.FEval(t.Context(), mockLogger, entities.FEvalRequest{Function: "invalid_function"})

	// Assert
	require.Error(t, err)
	assert.Contains(t, err.Error(), "response was in error state but no fault messages received")
	assert.Nil(t, response.Outputs)
}

func TestClient_FEval_NoResponseMessages(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	responsePayload := embeddedconnector.ConnectorPayload{
		Messages: embeddedconnector.ConnectorMessage{
			FevalResponse: []embeddedconnector.FevalResponseMessage{},
		},
	}
	responseBody, _ := json.Marshal(responsePayload)

	mockHttpClient.EXPECT().
		Do(mock.MatchedBy(validateConnectorRequest)).
		Return(&http.Response{
			StatusCode: http.StatusOK,
			Body:       io.NopCloser(bytes.NewReader(responseBody)),
		}, nil).
		Once()

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)

	// Act
	response, err := client.FEval(t.Context(), mockLogger, entities.FEvalRequest{Function: "sum"})

	// Assert
	require.Error(t, err)
	assert.Contains(t, err.Error(), "no response messages received")
	assert.Empty(t, response)
}

func TestClient_FEval_InvalidJSONResponse(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	mockHttpClient.EXPECT().
		Do(mock.MatchedBy(validateConnectorRequest)).
		Return(&http.Response{
			StatusCode: http.StatusOK,
			Body:       io.NopCloser(bytes.NewReader([]byte("invalid json"))),
		}, nil).
		Once()

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)

	// Act
	response, err := client.FEval(t.Context(), mockLogger, entities.FEvalRequest{Function: "sum"})

	// Assert
	require.Error(t, err)
	assert.Contains(t, err.Error(), "failed to unmarshal response")
	assert.Empty(t, response)
}

func TestClient_FEval_DoErrors(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	mockHttpClient.EXPECT().
		Do(mock.MatchedBy(validateConnectorRequest)).
		Return(nil, assert.AnError).
		Once()

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)

	ctx := t.Context()
	fevalRequest := entities.FEvalRequest{}

	// Act
	response, err := client.FEval(ctx, mockLogger, fevalRequest)

	// Assert
	require.Error(t, err)
	assert.Empty(t, response)
}

func TestClient_FEval_ContextPropagation(t *testing.T) {
	// Arrange
	mockLogger := testutils.NewInspectableLogger()

	mockHttpClient := &httpclientmocks.MockHttpClient{}
	defer mockHttpClient.AssertExpectations(t)

	type contextKeyType string
	const contextKey contextKeyType = "uniqueKey"
	const contextKeyValue = "uniqueValue"

	expectedContext := context.WithValue(t.Context(), contextKey, contextKeyValue)

	mockHttpClient.EXPECT().
		Do(mock.MatchedBy(func(request *http.Request) bool {
			return request.Context().Value(contextKey) == contextKeyValue
		})).
		Return(nil, assert.AnError).
		Once()

	client := embeddedconnector.Client{}
	client.SetHttpClient(mockHttpClient)

	fevalRequest := entities.FEvalRequest{}

	// Act
	response, err := client.FEval(expectedContext, mockLogger, fevalRequest)

	// Assert
	require.Error(t, err)
	assert.Empty(t, response)
}
