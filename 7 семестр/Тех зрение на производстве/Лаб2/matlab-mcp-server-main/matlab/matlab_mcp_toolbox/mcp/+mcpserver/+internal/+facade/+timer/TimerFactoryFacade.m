classdef (Abstract) TimerFactoryFacade
    %TimerFactoryFacade Abstract factory for creating TimerFacade instances

    % Copyright 2026 The MathWorks, Inc.

    methods (Abstract)
        t = timer(obj, period, executionMode, busyMode, timerFcn);
    end

end
