classdef (Abstract) FigureVisibilityController < handle
    %FigureVisibilityController Abstract interface for figure visibility control
    %   This abstract class defines the interface for controlling figure
    %   visibility during MCP server operations.

    % Copyright 2026 The MathWorks, Inc.

    methods (Abstract)
        hide(obj)
        show(obj)
        restore(obj)
    end

end
