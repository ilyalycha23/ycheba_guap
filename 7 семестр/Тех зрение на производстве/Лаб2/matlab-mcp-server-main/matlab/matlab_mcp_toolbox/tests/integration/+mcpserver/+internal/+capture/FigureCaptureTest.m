classdef FigureCaptureTest < mcpserver.internal.capture.CaptureTestHelper
    %FigureCaptureTest Integration tests for figure event capture

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testFigure_ProducesFigureEvent(testCase)
            evalin('base', "f = figure(Visible='off');");
            testCase.addTeardown(@() evalin('base', "close(f)"));
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'figure');

            testCase.verifyNotEmpty(events, "figure() should produce a figure event");
            testCase.verifyTrue(ishghandle(events(1).payload), ...
                "Figure event payload should be a valid graphics handle");
        end

        function testUifigure_ProducesFigureEvent(testCase)
            evalin('base', "uf = uifigure(Visible='off');");
            testCase.addTeardown(@() evalin('base', "close(uf)"));
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'figure');

            testCase.verifyNotEmpty(events, "uifigure() should produce a figure event");
            testCase.verifyTrue(ishghandle(events(1).payload), ...
                "Uifigure event payload should be a valid graphics handle");
        end

        function testPlot_ProducesFigureEvent(testCase)
            originalVisible = get(0, 'DefaultFigureVisible');
            testCase.addTeardown(@() set(0, 'DefaultFigureVisible', originalVisible));

            set(0, 'DefaultFigureVisible', 'off');
            evalin('base', "f = figure; plot(1:5);");
            set(0, 'DefaultFigureVisible', originalVisible);
            testCase.addTeardown(@() evalin('base', "close(f)"));
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'figure');

            testCase.verifyNotEmpty(events, "plot() should produce a figure event");
        end
    end

end
