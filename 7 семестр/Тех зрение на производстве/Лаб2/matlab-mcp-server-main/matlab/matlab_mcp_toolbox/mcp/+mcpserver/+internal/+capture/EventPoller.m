classdef (Abstract) EventPoller < mcpserver.internal.capture.CapturedEventProvider
    %EventPoller Abstract interface for polling and displaying events during execution

    % Copyright 2026 The MathWorks, Inc.

    methods (Abstract)
        start(obj)
        stop(obj)
        flush(obj)
    end

end
