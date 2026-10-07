classdef (Abstract) DisplayFacade
    %DisplayFacade Abstract facade for display and figure operations
    %   This abstract class defines the interface for MATLAB root graphics
    %   and figure operations.

    % Copyright 2026 The MathWorks, Inc.

    methods (Abstract)
        value = getRootProperty(obj, propertyName)
        setRootProperty(obj, propertyName, value)
        listener = addPropertyListener(obj, source, propertyName, eventType, callback)
    end

end
