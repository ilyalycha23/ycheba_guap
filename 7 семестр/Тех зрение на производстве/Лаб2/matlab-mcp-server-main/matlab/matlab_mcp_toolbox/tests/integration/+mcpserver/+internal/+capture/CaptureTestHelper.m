classdef (Abstract) CaptureTestHelper < matlab.unittest.TestCase
    %CaptureTestHelper Shared setup for capture functional tests

    % Copyright 2026 The MathWorks, Inc.

    properties (Access = protected)
        Capture
        EventProvider
    end

    methods (TestMethodSetup)
        function setupCaptureStack(testCase)
            testCase.EventProvider = mcpserver.internal.capture.DefaultCapturedEventProvider();
            testCase.Capture = mcpserver.internal.capture.DefaultOutputCapture();
            testCase.Capture.enable();

            testCase.addTeardown(@() testCase.Capture.disable());
            testCase.addTeardown(@() delete(testCase.EventProvider));
        end
    end

    methods (TestMethodTeardown)
        function cleanBaseWorkspace(~)
            evalin('base', 'clear');
        end
    end

    methods (Static, Access = protected)
        function filtered = filterByType(events, typeName)
            if isempty(events)
                filtered = events;
                return;
            end
            mask = arrayfun(@(e) strcmp(e.type, typeName), events);
            filtered = events(mask);
        end

        function text = joinStdout(events)
            text = strjoin({events.payload}, '');
        end
    end

end
