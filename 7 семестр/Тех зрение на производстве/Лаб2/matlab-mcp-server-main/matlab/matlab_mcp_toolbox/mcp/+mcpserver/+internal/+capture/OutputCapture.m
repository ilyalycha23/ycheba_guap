classdef (Abstract) OutputCapture < handle
    %OutputCapture Abstract interface for managing MATLAB output capture

    % Copyright 2026 The MathWorks, Inc.

    methods (Abstract)
        enable(obj)
        disable(obj)
        runUncaptured(obj, fcn)
    end

end
