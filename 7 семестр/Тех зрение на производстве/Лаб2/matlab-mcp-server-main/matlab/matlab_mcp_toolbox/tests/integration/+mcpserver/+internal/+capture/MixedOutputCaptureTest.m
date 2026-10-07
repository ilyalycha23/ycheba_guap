classdef MixedOutputCaptureTest < mcpserver.internal.capture.CaptureTestHelper
    %MixedOutputCaptureTest Integration tests for mixed output and edge cases

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testMixedOutput_StdoutAndVariableDisplay(testCase)
            evalin('base', "disp('text output'); x = 42");
            drawnow;
            testCase.Capture.disable();

            allEvents = testCase.EventProvider.getEvents();

            stdoutEvents = testCase.filterByType(allEvents, 'stdout');
            varEvents = testCase.filterByType(allEvents, 'VariableDisplay');

            testCase.verifyNotEmpty(stdoutEvents, "Should capture stdout");
            testCase.verifyNotEmpty(varEvents, "Should capture variable display");
        end

        function testMixedOutput_StdoutAndWarning(testCase)
            evalin('base', "disp('text output'); warning('test:mix', 'careful')");
            drawnow;
            testCase.Capture.disable();

            allEvents = testCase.EventProvider.getEvents();

            stdoutEvents = testCase.filterByType(allEvents, 'stdout');
            warnEvents = testCase.filterByType(allEvents, 'IssuedWarning');

            testCase.verifyNotEmpty(stdoutEvents, "Should capture stdout");
            testCase.verifyNotEmpty(warnEvents, "Should capture warning");
        end

        function testMixedOutput_FigureWithStdout(testCase)
            evalin('base', "f = figure(Visible='off');");
            testCase.addTeardown(@() evalin('base', "close(f)"));
            evalin('base', "disp('after figure')");
            drawnow;
            testCase.Capture.disable();

            allEvents = testCase.EventProvider.getEvents();

            figEvents = testCase.filterByType(allEvents, 'figure');
            stdoutEvents = testCase.filterByType(allEvents, 'stdout');

            testCase.verifyNotEmpty(figEvents, "Should capture figure");
            testCase.verifyNotEmpty(stdoutEvents, "Should capture stdout alongside figure");
        end

        function testEmptyOutput_NoEvents(testCase)
            evalin('base', "x = 1;");
            drawnow;
            testCase.Capture.disable();

            events = testCase.EventProvider.getEvents();
            stdoutEvents = testCase.filterByType(events, 'stdout');
            varEvents = testCase.filterByType(events, 'VariableDisplay');

            testCase.verifyEmpty(stdoutEvents, "Suppressed assignment should produce no stdout");
            testCase.verifyEmpty(varEvents, "Suppressed assignment should produce no VariableDisplay");
        end
    end

end
