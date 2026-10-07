classdef (Abstract) CapturedEventProvider < handle
    %CapturedEventProvider Abstract interface for retrieving captured output events

    % Copyright 2026 The MathWorks, Inc.

    methods (Abstract)
        collectedEvents = getEvents(obj)
    end

end
