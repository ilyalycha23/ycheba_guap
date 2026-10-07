classdef StdoutDisplayTest < mcpserver.internal.display.console.DisplayTestHelper
    %StdoutDisplayTest Integration tests for stdout console display

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testDisp_String_DisplaysInConsole(testCase)
            consoleOutput = testCase.captureAndDisplay("disp('hello world')");

            testCase.verifySubstring(consoleOutput, "hello world");
        end

        function testFprintf_DisplaysInConsole(testCase)
            consoleOutput = testCase.captureAndDisplay("fprintf('value is %d\n', 42)");

            testCase.verifySubstring(consoleOutput, "value is 42");
        end

        function testMultipleDisp_DisplaysAll(testCase)
            consoleOutput = testCase.captureAndDisplay("disp('line1'); disp('line2')");

            testCase.verifySubstring(consoleOutput, "line1");
            testCase.verifySubstring(consoleOutput, "line2");
        end

    end

end
