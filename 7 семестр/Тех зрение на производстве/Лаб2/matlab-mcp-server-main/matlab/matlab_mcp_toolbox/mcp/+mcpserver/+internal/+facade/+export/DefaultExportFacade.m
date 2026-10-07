classdef DefaultExportFacade < mcpserver.internal.facade.export.ExportFacade
    %DefaultExportFacade Default implementation wrapping MATLAB builtins

    % Copyright 2026 The MathWorks, Inc.

    methods
        function exportgraphics(~, fig, filename, varargin)
            exportgraphics(fig, filename, varargin{:});
        end

        function path = tempname(~, varargin)
            path = string(tempname(varargin{:}));
        end

        function encoded = base64encode(~, bytes)
            encoded = matlab.net.base64encode(bytes);
        end
    end

end
