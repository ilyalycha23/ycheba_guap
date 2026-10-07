// Copyright 2026 The MathWorks, Inc.

package mcpbundle

func NewBundleForTest(bundleDir string, runner CommandRunner) *Bundle {
	return newBundle(bundleDir, runner)
}

func LauncherFilename() string {
	return launcherFilename
}
