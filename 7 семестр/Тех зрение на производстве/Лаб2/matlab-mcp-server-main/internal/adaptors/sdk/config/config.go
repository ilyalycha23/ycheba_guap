// Copyright 2026 The MathWorks, Inc.

package config

import (
	"reflect"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/messages"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/sdk/publictypes"
	internalmessages "github.com/matlab/matlab-mcp-server/internal/messages"
)

type InternalConfig interface {
	Get(key string) (any, internalmessages.Error)
}

type InternalMessageCatalog interface {
	GetFromError(err internalmessages.Error) string
}

type MessagesFactory interface {
	New(messageCatalog messages.MessageCatalog) messages.I18nErrorFactory
}

type Factory struct {
	messagesFactory MessagesFactory
}

func NewFactory(
	messagesFactory MessagesFactory,
) *Factory {
	return &Factory{
		messagesFactory: messagesFactory,
	}
}

func (f *Factory) New(
	internalConfig InternalConfig,
	internalMessageCatalog InternalMessageCatalog,
) publictypes.Config {
	return &configAdaptor{
		internalConfig: internalConfig,
		errorFactory:   f.messagesFactory.New(internalMessageCatalog),
	}
}

type configAdaptor struct {
	internalConfig InternalConfig
	errorFactory   messages.I18nErrorFactory
}

func (c *configAdaptor) Get(key string, expectedTypeZeroValue any) (any, publictypes.Error) {
	value, err := c.internalConfig.Get(key)
	if err != nil {
		return nil, c.errorFactory.FromInternalError(err)
	}

	valueType := reflect.TypeOf(value)
	expectedType := reflect.TypeOf(expectedTypeZeroValue)

	if expectedType == nil || valueType != expectedType {
		expectedTypeName := "<nil>"
		if expectedType != nil {
			expectedTypeName = expectedType.String()
		}
		internalError := internalmessages.New_StartupErrors_InvalidParameterType_Error(key, expectedTypeName)
		return nil, c.errorFactory.FromInternalError(internalError)
	}

	return value, nil
}
