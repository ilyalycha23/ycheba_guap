classdef (Abstract) TimerFacade < handle
    %TimerFacade Abstract facade for a single MATLAB timer instance

    % Copyright 2026 The MathWorks, Inc.

    methods (Abstract)
        Start(obj);
        Stop(obj);
    end

end
