classdef (Abstract) CollectorFactoryFacade
    %CollectorFactoryFacade Abstract factory for creating CollectorFacade instances

    % Copyright 2026 The MathWorks, Inc.

    methods (Abstract)
        collector = EventsCollector(obj);
    end

end
