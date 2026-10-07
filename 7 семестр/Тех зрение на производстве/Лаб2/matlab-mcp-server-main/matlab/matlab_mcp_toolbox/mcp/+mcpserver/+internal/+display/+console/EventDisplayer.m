classdef (Abstract) EventDisplayer < handle
    %EventDisplayer Abstract interface for displaying captured events to the console

    % Copyright 2026 The MathWorks, Inc.

    methods (Abstract)
        displayEvents(obj, capturedEvents)
    end

end
