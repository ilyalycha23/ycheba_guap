classdef (Abstract) ExportFacade
    %ExportFacade Abstract facade for figure export operations

    % Copyright 2026 The MathWorks, Inc.

    methods (Abstract)
        exportgraphics(obj, fig, filename, varargin)
        path = tempname(obj, varargin)
        encoded = base64encode(obj, bytes)
    end

end
