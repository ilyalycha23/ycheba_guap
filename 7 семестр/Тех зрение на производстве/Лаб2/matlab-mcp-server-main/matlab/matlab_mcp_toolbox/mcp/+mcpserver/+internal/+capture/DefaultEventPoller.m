classdef DefaultEventPoller < mcpserver.internal.capture.EventPoller
    %DefaultEventPoller Timer-based implementation that displays events periodically

    % Copyright 2026 The MathWorks, Inc.

    properties (Constant, Access = private)
        DefaultPollPeriod = 0.25
    end

    properties (GetAccess = private, SetAccess = immutable)
        TimerFactory(1, 1) mcpserver.internal.facade.timer.TimerFactoryFacade = mcpserver.internal.facade.timer.DefaultTimerFactoryFacade()
        EventSource
        Displayer
    end

    properties (SetAccess = private)
        RealEvents = []
    end

    properties (Access = private)
        Timer
        LastDisplayedIdx double = 0
        IsFlushing logical = false
    end

    methods
        function obj = DefaultEventPoller(options)
            arguments
                options.?mcpserver.internal.capture.DefaultEventPoller
            end

            for prop = string(fieldnames(options).')
                obj.(prop) = options.(prop);
            end

            obj.Timer = obj.TimerFactory.timer( ...
                obj.DefaultPollPeriod, 'fixedRate', 'drop', ...
                @(~, ~) obj.flush());
        end

        function start(obj)
            obj.Timer.Start();
        end

        function stop(obj)
            if ~isempty(obj.Timer) && isvalid(obj.Timer)
                obj.Timer.Stop();
            end
        end

        function flush(obj)
            if obj.IsFlushing
                return;
            end
            obj.IsFlushing = true;
            cleanup = onCleanup(@() obj.clearFlushing());

            events = obj.EventSource.getEvents();
            numEvents = numel(events);
            if obj.LastDisplayedIdx < numEvents
                newEvents = events(obj.LastDisplayedIdx+1:numEvents);
                if isempty(obj.RealEvents)
                    obj.RealEvents = newEvents;
                else
                    obj.RealEvents(end+1:end+numel(newEvents)) = newEvents;
                end
                obj.Displayer.displayEvents(newEvents);
            end
            obj.LastDisplayedIdx = numEvents;
        end

        function collectedEvents = getEvents(obj)
            collectedEvents = obj.RealEvents;
        end

        function delete(obj)
            obj.stop();
        end
    end

    methods (Access = private)
        function clearFlushing(obj)
            obj.IsFlushing = false;
        end
    end

end
