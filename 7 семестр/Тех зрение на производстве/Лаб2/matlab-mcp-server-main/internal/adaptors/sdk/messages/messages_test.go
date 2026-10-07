// Copyright 2026 The MathWorks, Inc.

package messages_test

import (
	"testing"

	messagesadaptor "github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/messages"
	internalmessages "github.com/matlab/matlab-mcp-server/internal/messages"
	messagesmocks "github.com/matlab/matlab-mcp-server/mocks/adaptors/sdk/messages"
	"github.com/stretchr/testify/require"
)

func TestNewFactory_HappyPath(t *testing.T) {
	// Arrange
	// Act
	factory := messagesadaptor.NewFactory()

	// Assert
	require.NotNil(t, factory)
}

func TestFactory_New_HappyPath(t *testing.T) {
	// Arrange
	mockMessageCatalog := &messagesmocks.MockMessageCatalog{}
	defer mockMessageCatalog.AssertExpectations(t)

	// Act
	errorFactory := messagesadaptor.NewFactory().New(mockMessageCatalog)

	// Assert
	require.NotNil(t, errorFactory)
}

func TestI18nErrorFactory_FromInternalError_HappyPath(t *testing.T) {
	// Arrange
	mockMessageCatalog := &messagesmocks.MockMessageCatalog{}
	defer mockMessageCatalog.AssertExpectations(t)

	expectedErrorMessage := "translated error message"

	mockMessageCatalog.EXPECT().
		GetFromError(internalmessages.AnError).
		Return(expectedErrorMessage).
		Once()

	factory := messagesadaptor.NewFactory().New(mockMessageCatalog)

	// Act
	result := factory.FromInternalError(internalmessages.AnError)

	// Assert
	require.Error(t, result)
	require.Equal(t, expectedErrorMessage, result.Error())
}
