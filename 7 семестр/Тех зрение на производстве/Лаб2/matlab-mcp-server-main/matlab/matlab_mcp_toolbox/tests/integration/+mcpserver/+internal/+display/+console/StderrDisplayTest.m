classdef StderrDisplayTest < mcpserver.internal.display.console.DisplayTestHelper
    %StderrDisplayTest Integration tests for stderr console display

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testStderr_DisplaysInConsole(testCase)
            displayer = mcpserver.internal.display.console.DefaultEventDisplayer(); %#ok<NASGU>

            stderrEvent = struct('type', 'stderr', 'payload', 'error text'); %#ok<NASGU>

            consoleOutput = evalc('displayer.displayEvents(stderrEvent)');

            testCase.verifySubstring(consoleOutput, "error text");
        end
    end

end
