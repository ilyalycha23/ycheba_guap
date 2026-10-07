classdef WarningCaptureTest < mcpserver.internal.capture.CaptureTestHelper
    %WarningCaptureTest Functional tests for IssuedWarning event capture

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testWarning_ProducesIssuedWarningEvent(testCase)
            evalin('base', "warning('test:w', 'watch out')");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'IssuedWarning');

            testCase.verifyNotEmpty(events, "warning() should produce an IssuedWarning event");
            testCase.verifyEqual(string(events(1).payload.identifier), "test:w");
            testCase.verifySubstring(events(1).payload.message, "watch out");
            testCase.verifyFalse(events(1).payload.wasDisabled);
        end

        function testDisabledWarning_ProducesIssuedWarningWithFlag(testCase)
            evalin('base', "warning('off', 'test:dw'); warning('test:dw', 'silenced'); warning('on', 'test:dw')");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'IssuedWarning');
            disabled = events(arrayfun(@(e) e.payload.wasDisabled, events));

            testCase.verifyNotEmpty(disabled, ...
                "A disabled warning should still produce an IssuedWarning with wasDisabled=true");
            testCase.verifyTrue(disabled(1).payload.wasDisabled);
        end
    end

end
