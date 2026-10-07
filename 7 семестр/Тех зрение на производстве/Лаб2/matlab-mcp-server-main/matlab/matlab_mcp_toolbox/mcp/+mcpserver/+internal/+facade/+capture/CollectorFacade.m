classdef (Abstract) CollectorFacade < handle
    %CollectorFacade Abstract facade for a single MATLAB EventsCollector instance

    % Copyright 2026 The MathWorks, Inc.

    methods (Abstract)
        collectedEvents = Events(obj)
    end

end
