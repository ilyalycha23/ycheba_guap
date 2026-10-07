// Copyright 2026 The MathWorks, Inc.

package mcpb_test

import (
	"slices"
	"testing"

	"github.com/matlab/matlab-mcp-server/tests/testutils/mcpbundle"
	"github.com/matlab/matlab-mcp-server/tests/testutils/mcpserver"
	"github.com/stretchr/testify/suite"
)

// MCPBBundleParitySuite verifies the bundle metadata (version, flags) matches what the binary reports.
type MCPBBundleParitySuite struct {
	suite.Suite

	bundle *mcpbundle.Bundle
}

func (s *MCPBBundleParitySuite) SetupSuite() {
	s.bundle = mcpbundle.Open(s.T())
}

func TestMCPBBundleParitySuite(t *testing.T) {
	suite.Run(t, new(MCPBBundleParitySuite))
}

func (s *MCPBBundleParitySuite) TestVersion_MatchesBinary() {
	manifestVersion, err := s.bundle.ManifestVersion()
	s.Require().NoError(err)

	binaryVersion := mcpserver.Run(s.T(), s.bundle.BinaryPath(), []string{"--version"}, nil)
	parsedVersion, err := mcpserver.ParseVersion(binaryVersion)
	s.Require().NoError(err)

	s.Require().NotEqual("(devel)", parsedVersion,
		"binary reports (devel) — it was not built correctly")
	s.Equal(manifestVersion, parsedVersion,
		"manifest version should match binary version")
}

func (s *MCPBBundleParitySuite) TestFlags_MatchBinary() {
	helpOutput := mcpserver.Run(s.T(), s.bundle.BinaryPath(), []string{"--help"}, nil)
	binaryFlags := mcpserver.ParseHelpFlags(helpOutput)

	launcherFlags, err := s.bundle.LauncherFlags()
	s.Require().NoError(err)

	expectedFlags := slices.DeleteFunc(binaryFlags, func(flag string) bool {
		_, excluded := mcpbundle.ExcludedFlags()[flag]
		return excluded
	})

	s.ElementsMatch(expectedFlags, launcherFlags,
		"launcher flags should match binary flags (minus ExcludedFlags)")
}
