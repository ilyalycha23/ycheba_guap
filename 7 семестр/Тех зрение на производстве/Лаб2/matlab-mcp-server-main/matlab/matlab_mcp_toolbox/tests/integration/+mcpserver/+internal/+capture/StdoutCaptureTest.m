classdef StdoutCaptureTest < mcpserver.internal.capture.CaptureTestHelper
    %StdoutCaptureTest Functional tests for stdout event capture

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testDisp_String_ProducesStdoutEvent(testCase)
            evalin('base', "disp('hello world')");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'stdout');

            testCase.verifyNotEmpty(events, "disp should produce a stdout event");
            allText = testCase.joinStdout(events);
            testCase.verifySubstring(allText, "hello world");
        end

        function testFprintf_ProducesStdoutEvent(testCase)
            evalin('base', "fprintf('value is %d\n', 42)");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'stdout');

            testCase.verifyNotEmpty(events, "fprintf should produce a stdout event");
            allText = testCase.joinStdout(events);
            testCase.verifySubstring(allText, "value is 42");
        end

        function testDispMultipleLines_ProducesStdoutEvents(testCase)
            evalin('base', "disp('line1'); disp('line2')");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'stdout');

            testCase.verifyNotEmpty(events, ...
                "Multiple disp calls should produce stdout events");
            allText = testCase.joinStdout(events);
            testCase.verifySubstring(allText, "line1");
            testCase.verifySubstring(allText, "line2");
        end
    end

end
