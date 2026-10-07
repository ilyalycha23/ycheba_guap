// Copyright 2026 The MathWorks, Inc.

package testbinaries

import (
	"bytes"
	"embed"
	"io/fs"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
	"text/template"

	"github.com/matlab/matlab-mcp-server/tests/testconfig"

	"github.com/stretchr/testify/require"
)

//go:embed source
var source embed.FS

const goModName = "mathworks.com/sdk-module"
const goModTemplate = `module ` + goModName + `

replace github.com/matlab/matlab-mcp-server => {{ .SDKPath }}
`

func BuildEmptyServer(t *testing.T) ServerDetails {
	// Those string literals match the one in the source code
	return ServerDetails{
		binaryLocation: buildSDKServer(t, "empty_server"),

		moduleName: goModName,

		name:         "empty-server",
		title:        "Empty Server",
		instructions: "This is the Empty Server test binary",
	}
}

func BuildServerWithCustomParameters(t *testing.T) ServerWithCustomParametersDetails {
	// Those string literals match the one in the source code
	return ServerWithCustomParametersDetails{
		ServerDetails: ServerDetails{
			binaryLocation: buildSDKServer(t, "server_with_custom_parameters"),

			moduleName: goModName,

			name:         "server-with-custom-parameters",
			title:        "Server With Custom Parameters",
			instructions: "This is a test server with custom parameters",
		},

		greetToolName:               "greet",
		greetStructuredToolName:     "greet-structured",
		customParamFlagName:         "custom-param",
		customRecordedParamFlagName: "custom-recorded-param",
		customRecordedParamID:       "custom-recorded-param-id",
		customRecordedParamEnvVar:   "CUSTOM_RECORDED_PARAM",
	}
}

func BuildServerWithCustomTools(t *testing.T) ServerWithCustomToolsDetails {
	// Those string literals match the one in the source code
	return ServerWithCustomToolsDetails{
		ServerDetails: ServerDetails{
			binaryLocation: buildSDKServer(t, "server_with_custom_tools"),

			moduleName: goModName,

			name:         "server-with-custom-tools",
			title:        "Server With Custom Tools",
			instructions: "This is a test server with custom tools",
		},

		greetToolName:           "greet",
		greetStructuredToolName: "greet-structured",
	}
}

func BuildServerWithMATLABFeature(t *testing.T) ServerDetails {
	// Those string literals match the one in the source code
	return ServerDetails{
		binaryLocation: buildSDKServer(t, "server_with_matlab_feature"),

		moduleName: goModName,

		name:         "server-with-matlab-feature",
		title:        "Server With MATLAB Feature",
		instructions: "This is a test server with MATLAB feature",
	}
}

func BuildServerWithCustomDependencies(t *testing.T) ServerWithCustomDependenciesDetails {
	// Those string literals match the one in the source code
	return ServerWithCustomDependenciesDetails{
		ServerDetails: ServerDetails{
			binaryLocation: buildSDKServer(t, "server_with_custom_dependencies"),

			moduleName: goModName,

			name:         "server-with-custom-dependencies",
			title:        "Server With Custom Dependencies",
			instructions: "This is a test server with custom dependencies",
		},

		greetToolName: "greet",
	}
}

func BuildServerWithWatchdog(t *testing.T) ServerWithWatchdogDetails {
	// Those string literals match the one in the source code
	return ServerWithWatchdogDetails{
		ServerDetails: ServerDetails{
			binaryLocation: buildSDKServer(t, "server_with_watchdog"),

			moduleName: goModName,

			name:         "server-with-watchdog",
			title:        "Server With Watchdog",
			instructions: "This is a test server with watchdog",
		},

		getPIDToolName: "get-pid",
	}
}

func BuildServerWithLogging(t *testing.T) ServerWithLoggingDetails {
	// Those string literals match the one in the source code
	return ServerWithLoggingDetails{
		ServerDetails: ServerDetails{
			binaryLocation: buildSDKServer(t, "server_with_logging"),

			moduleName: goModName,

			name:         "server-with-logging",
			title:        "Server With Logging",
			instructions: "This is a test server focused on logging",
		},

		toolThatLogsName:           "tool-that-logs",
		structuredToolThatLogsName: "structured-tool-that-logs",
	}
}

func buildSDKServer(t *testing.T, serverFolder string) string {
	t.Helper()

	tempDir := t.TempDir()

	sourcePath := copySDKServerSourceFiles(t, serverFolder)

	cmd := exec.Command("go",
		"mod",
		"tidy",
	)
	cmd.Dir = sourcePath

	output, err := cmd.CombinedOutput()
	require.NoError(t, err, "go mod tidy failed: %s", string(output))

	serverBinaryPath := filepath.Join(tempDir, "test_server"+testconfig.ExecutableExtension)

	cmd = exec.Command("go", //nolint:gosec // Trusted variable
		"build",
		"-o",
		serverBinaryPath,
		".",
	)
	cmd.Dir = sourcePath

	output, err = cmd.CombinedOutput()
	require.NoError(t, err, "go build failed: %s", string(output))

	return serverBinaryPath
}

func copySDKServerSourceFiles(t *testing.T, serverFolder string) string {
	t.Helper()

	sourceDir := filepath.Join(t.TempDir(), "source", serverFolder)
	sourceFS, err := fs.Sub(source, "source/"+serverFolder)
	require.NoError(t, err)

	err = fs.WalkDir(sourceFS, ".", func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		targetPath := filepath.Join(sourceDir, path)
		if d.IsDir() {
			return os.MkdirAll(targetPath, 0750)
		}
		content, err := fs.ReadFile(sourceFS, path)
		if err != nil {
			return err
		}
		return os.WriteFile(targetPath, content, 0600)
	})
	require.NoError(t, err, "failed to copy embedded source files")

	sdkPath := getSDKPath(t)
	writeGoMod(t, sourceDir, sdkPath)

	return sourceDir
}

func getSDKPath(t *testing.T) string {
	t.Helper()

	cmd := exec.Command("go", "env", "GOMOD")
	output, err := cmd.Output()
	require.NoError(t, err, "failed to run 'go env GOMOD'")

	goModPath := strings.TrimSpace(string(output))
	require.NotEmpty(t, goModPath, "go env GOMOD returned empty path")

	return filepath.Dir(goModPath)
}

type goModData struct {
	SDKPath string
}

func writeGoMod(t *testing.T, dir string, sdkPath string) {
	t.Helper()

	tmpl, err := template.New("go.mod").Parse(goModTemplate)
	require.NoError(t, err, "failed to parse go.mod template")

	data := goModData{
		SDKPath: sdkPath,
	}

	var buf bytes.Buffer
	err = tmpl.Execute(&buf, data)
	require.NoError(t, err, "failed to execute go.mod template")

	goModPath := filepath.Join(dir, "go.mod")
	err = os.WriteFile(goModPath, buf.Bytes(), 0600)
	require.NoError(t, err, "failed to write go.mod file")
}
