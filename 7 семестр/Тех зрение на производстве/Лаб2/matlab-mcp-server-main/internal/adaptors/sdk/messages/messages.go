// Copyright 2026 The MathWorks, Inc.

package messages

import (
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
	internalmessages "github.com/matlab/matlab-mcp-server/internal/messages"
)

type MessageCatalog interface {
	GetFromError(err internalmessages.Error) string
}

type I18nErrorFactory interface {
	FromInternalError(internalError internalmessages.Error) publictypes.Error
}

type Factory struct{}

func NewFactory() *Factory {
	return &Factory{}
}

type messagesAdaptor struct {
	messageCatalog MessageCatalog
}

func (f *Factory) New(messageCatalog MessageCatalog) I18nErrorFactory {
	return &messagesAdaptor{
		messageCatalog: messageCatalog,
	}
}

func (a *messagesAdaptor) FromInternalError(internalError internalmessages.Error) publictypes.Error {
	message := a.messageCatalog.GetFromError(internalError)
	return &i18nErrorFromInternalError{
		message: message,
	}
}

type i18nErrorFromInternalError struct {
	message string
}

func (e *i18nErrorFromInternalError) Error() string {
	return e.message
}

func (e *i18nErrorFromInternalError) MWMarker() {}
