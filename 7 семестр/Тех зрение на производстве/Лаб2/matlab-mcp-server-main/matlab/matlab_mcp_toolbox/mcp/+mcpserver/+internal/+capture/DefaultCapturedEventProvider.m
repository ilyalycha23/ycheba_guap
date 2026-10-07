classdef DefaultCapturedEventProvider < mcpserver.internal.capture.CapturedEventProvider
    %DefaultCapturedEventProvider Implementation using MATLAB internal EventsCollector

    % Copyright 2026 The MathWorks, Inc.

    properties (GetAccess = private, SetAccess = immutable)
        Factory(1, 1) mcpserver.internal.facade.capture.CollectorFactoryFacade = mcpserver.internal.facade.capture.DefaultCollectorFactoryFacade()
    end

    properties (Access = private)
        Collector
    end

    methods
        function obj = DefaultCapturedEventProvider(options)
            arguments
                options.?mcpserver.internal.capture.DefaultCapturedEventProvider
            end

            for prop = string(fieldnames(options).')
                obj.(prop) = options.(prop);
            end

            obj.Collector = obj.Factory.EventsCollector();
        end

        function collectedEvents = getEvents(obj)
            collectedEvents = obj.Collector.Events();
        end

        function delete(obj)
            if ~isempty(obj.Collector)
                delete(obj.Collector);
            end
        end
    end

end
