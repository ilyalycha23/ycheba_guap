classdef DefaultDisplayFacade < mcpserver.internal.facade.display.DisplayFacade
    %DefaultDisplayFacade Default implementation for display and figure operations
    %   This class delegates to MATLAB's built-in root graphics and figure
    %   functions.

    % Copyright 2026 The MathWorks, Inc.

    methods
        function value = getRootProperty(~, propertyName)
            value = get(0, propertyName);
        end

        function setRootProperty(~, propertyName, value)
            set(0, propertyName, value);
        end

        function listener = addPropertyListener(~, source, propertyName, eventType, callback)
            listener = addlistener(source, propertyName, eventType, callback);
        end
    end

end
