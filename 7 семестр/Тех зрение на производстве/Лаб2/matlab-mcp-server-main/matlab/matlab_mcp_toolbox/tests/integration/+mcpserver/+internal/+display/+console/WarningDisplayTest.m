classdef WarningDisplayTest < mcpserver.internal.display.console.DisplayTestHelper
    %WarningDisplayTest Integration tests for warning console display

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testWarning_WithIdentifier_DisplaysMessage(testCase)
            consoleOutput = testCase.captureAndDisplay( ...
                "warning('mylib:test', 'Something fishy')");

            testCase.verifySubstring(consoleOutput, "Something fishy");
        end

        function testWarning_WithoutIdentifier_DisplaysMessage(testCase)
            consoleOutput = testCase.captureAndDisplay( ...
                "warning('no id warning')");

            testCase.verifySubstring(consoleOutput, "no id warning");
        end

        function testWarning_BacktraceSetting_Preserved(testCase)
            original = warning('query', 'backtrace');

            testCase.captureAndDisplay( ...
                "warning('test:bt', 'backtrace test')");

            current = warning('query', 'backtrace');
            testCase.verifyEqual(current.state, original.state);
        end

        function testDisabledWarning_NotDisplayed(testCase)
            consoleOutput = testCase.captureAndDisplay( ...
                "warning('off', 'test:dw'); warning('test:dw', 'silenced'); warning('on', 'test:dw')");

            testCase.verifyThat(consoleOutput, ...
                ~matlab.unittest.constraints.ContainsSubstring("silenced"), ...
                "A disabled warning should not be displayed");
        end
    end

end
