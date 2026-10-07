classdef Base64PngFigureConverter < mcpserver.internal.output.converter.Converter
    %Base64PngFigureConverter Converts figure handles to base64-encoded PNG

    % Copyright 2026 The MathWorks, Inc.

    properties (Constant)
        DefaultResolution(1, 1) double = 150
    end

    properties (GetAccess = private, SetAccess = immutable)
        AppDataLocator(1, 1) mcpserver.internal.appdata.AppDataLocator = mcpserver.internal.appdata.DefaultAppDataLocator()
        FSAdaptor(1, 1) mcpserver.internal.fs.FSAdaptor = mcpserver.internal.fs.DefaultFSAdaptor()
        ExportFacade(1, 1) mcpserver.internal.facade.export.ExportFacade = mcpserver.internal.facade.export.DefaultExportFacade()
        FSFacade(1, 1) mcpserver.internal.facade.fs.FSFacade = mcpserver.internal.facade.fs.DefaultFSFacade()
        Resolution(1, 1) double = mcpserver.internal.output.converter.Base64PngFigureConverter.DefaultResolution
    end

    methods
        function obj = Base64PngFigureConverter(options)
            arguments
                options.?mcpserver.internal.output.converter.Base64PngFigureConverter
            end

            for prop = string(fieldnames(options).')
                obj.(prop) = options.(prop);
            end
        end

        function out = convert(obj, evt)
            figHandle = evt.payload;

            figuresFolder = fullfile(obj.AppDataLocator.getAppDataFolder(), "v1", "figures");
            obj.FSAdaptor.ensureSecureFolder(figuresFolder);

            tmpPath = obj.ExportFacade.tempname(figuresFolder) + ".png";
            cleanup = onCleanup(@() obj.deleteTempFile(tmpPath));

            obj.ExportFacade.exportgraphics(figHandle, tmpPath, 'Resolution', obj.Resolution);

            bytes = obj.readFileBytes(tmpPath);
            b64 = obj.ExportFacade.base64encode(bytes);

            out = struct( ...
                'outputType', 'figure', ...
                'mimeType', 'image/png', ...
                'data', char(b64) ...
            );
        end
    end

    methods (Access = private)
        function bytes = readFileBytes(obj, path)
            fid = obj.FSFacade.fopen(path, 'r');
            if fid == -1
                throw(mcpserver.internal.error.Errors.FailedToReadFile(path));
            end
            cleanup = onCleanup(@() obj.FSFacade.fclose(fid));
            bytes = obj.FSFacade.fread(fid, Inf, '*uint8');
        end

        function deleteTempFile(obj, path)
            try
                obj.FSFacade.delete(path);
            catch
            end
        end
    end

end
