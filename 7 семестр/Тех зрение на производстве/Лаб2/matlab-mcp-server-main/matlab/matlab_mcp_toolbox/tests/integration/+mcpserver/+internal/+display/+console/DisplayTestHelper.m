classdef (Abstract) DisplayTestHelper < matlab.unittest.TestCase
    %DisplayTestHelper Shared setup for display integration tests

    % Copyright 2026 The MathWorks, Inc.

    properties (Access = protected)
        Capture
        EventProvider
    end

    methods (TestMethodSetup)
        function setupCapture(testCase)
            testCase.EventProvider = mcpserver.internal.capture.DefaultCapturedEventProvider();
            testCase.Capture = mcpserver.internal.capture.DefaultOutputCapture();
            testCase.addTeardown(@() testCase.Capture.disable());
            testCase.addTeardown(@() delete(testCase.EventProvider));
        end
    end

    methods (TestMethodTeardown)
        function cleanBaseWorkspace(~)
            evalin('base', 'clear');
        end
    end

    methods (Access = protected)
        function consoleOutput = captureAndDisplay(testCase, code)
            testCase.Capture.enable();
            try
                evalin('base', code);
            catch
                % Errors are not relevant; we only care about captured events.
            end
            drawnow;
            testCase.Capture.disable();

            capturedEvents = testCase.EventProvider.getEvents(); %#ok<NASGU>
            displayer = mcpserver.internal.display.console.DefaultEventDisplayer(); %#ok<NASGU>

            consoleOutput = evalc('displayer.displayEvents(capturedEvents)');
        end
    end

end
