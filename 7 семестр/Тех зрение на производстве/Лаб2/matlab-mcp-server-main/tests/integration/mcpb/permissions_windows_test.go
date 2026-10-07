// Copyright 2026 The MathWorks, Inc.

package mcpb_test

import (
	"os"
	"testing"

	"github.com/stretchr/testify/require"
)

func assertLauncherPermissions(t *testing.T, launcherSh, launcherCmd string) {
	t.Helper()

	_, err := os.Stat(launcherSh)
	require.NoError(t, err)

	_, err = os.Stat(launcherCmd)
	require.NoError(t, err)
}
