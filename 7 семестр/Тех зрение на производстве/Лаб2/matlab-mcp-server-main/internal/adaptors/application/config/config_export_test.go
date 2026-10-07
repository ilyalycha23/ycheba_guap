// Copyright 2025-2026 The MathWorks, Inc.

package config

import (
	"github.com/matlab/matlab-mcp-server/internal/messages"
)

const RedactedValue = redactedValue

func NewConfig(osLayer OSLayer, parser Parser, buildInfo BuildInfo) (*config, messages.Error) {
	return newConfig(osLayer, parser, buildInfo)
}
