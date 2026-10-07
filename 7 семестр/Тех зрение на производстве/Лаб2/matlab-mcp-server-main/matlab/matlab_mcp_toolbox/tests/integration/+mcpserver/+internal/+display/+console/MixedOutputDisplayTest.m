classdef MixedOutputDisplayTest < mcpserver.internal.display.console.DisplayTestHelper
    %MixedOutputDisplayTest Integration tests for mixed output console display

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testStdoutAndWarning_DisplaysBoth(testCase)
            consoleOutput = testCase.captureAndDisplay( ...
                "disp('text output'); warning('test:w', 'watch out')");

            testCase.verifySubstring(consoleOutput, "text output");
            testCase.verifySubstring(consoleOutput, "watch out");
        end

        function testUserError_DisplaysOutputBeforeError(testCase)
            consoleOutput = testCase.captureAndDisplay( ...
                "disp('before error'); error('test:e', 'boom')");

            testCase.verifySubstring(consoleOutput, "before error");
            testCase.verifyThat(consoleOutput, ...
                ~matlab.unittest.constraints.ContainsSubstring("boom"));
        end

        function testEmptyCode_NoOutput(testCase)
            consoleOutput = testCase.captureAndDisplay("% just a comment");

            testCase.verifyEqual(strtrim(consoleOutput), '');
        end

        function testSuppressedOnly_NoOutput(testCase)
            consoleOutput = testCase.captureAndDisplay("x = 1; y = 2; z = 3;");

            testCase.verifyEqual(strtrim(consoleOutput), '');
        end
    end

end
