// Copyright 2025-2026 The MathWorks, Inc.

package runmatlabtestfile

const (
	name        = "run_matlab_test_file"
	title       = "Run MATLAB test file"
	description = "Execute a MATLAB test script (`script_path`) using MATLAB's built-in runtests function and return comprehensive test results. Designed specifically for MATLAB unit test files that follow MATLAB's testing framework conventions."
)

type Args struct {
	ScriptPath string `json:"script_path" jsonschema:"The full absolute path to the MATLAB test script file. Must be a .m file containing MATLAB unit tests. Example: C:\\Users\\username\\tests\\testMyFunction.m or /home/user/matlab/tests/test_analysis.m."`
}
