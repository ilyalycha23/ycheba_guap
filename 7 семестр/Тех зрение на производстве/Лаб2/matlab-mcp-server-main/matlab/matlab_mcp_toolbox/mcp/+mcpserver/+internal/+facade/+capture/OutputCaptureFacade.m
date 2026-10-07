classdef (Abstract) OutputCaptureFacade
    %OutputCaptureFacade Abstract facade for MATLAB output capture builtins

    % Copyright 2026 The MathWorks, Inc.

    methods (Abstract)
        value = getAllowOutputCapture(obj)
        setAllowOutputCapture(obj, value)
        value = getSuppressCommandLineOutput(obj)
        setSuppressCommandLineOutput(obj, value)
        value = getHotlinks(obj)
        setHotlinks(obj, value)
        pushTextOutputListeners(obj)
        popTextOutputListeners(obj)
        resetStructuredFigures(obj)
    end

end
