classdef DefaultCollectorFacade < mcpserver.internal.facade.capture.CollectorFacade
    %DefaultCollectorFacade Wraps a single matlab.internal.structuredoutput.EventsCollector

    % Copyright 2026 The MathWorks, Inc.

    properties (Access = private)
        Collector
    end

    methods
        function obj = DefaultCollectorFacade()
            obj.Collector = matlab.internal.structuredoutput.EventsCollector();
        end

        function collectedEvents = Events(obj)
            collectedEvents = obj.Collector.Events;
        end

        function delete(obj)
            if ~isempty(obj.Collector) && isvalid(obj.Collector)
                delete(obj.Collector);
            end
        end
    end

end
