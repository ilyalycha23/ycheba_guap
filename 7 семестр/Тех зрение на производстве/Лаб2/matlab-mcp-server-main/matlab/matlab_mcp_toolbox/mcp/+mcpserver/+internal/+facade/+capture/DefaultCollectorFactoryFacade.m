classdef DefaultCollectorFactoryFacade < mcpserver.internal.facade.capture.CollectorFactoryFacade
    %DefaultCollectorFactoryFacade Creates DefaultCollectorFacade instances

    % Copyright 2026 The MathWorks, Inc.

    methods
        function collector = EventsCollector(~)
            collector = mcpserver.internal.facade.capture.DefaultCollectorFacade();
        end
    end

end
