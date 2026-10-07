classdef DefaultAppDataLocator < mcpserver.internal.appdata.AppDataLocator
    %DefaultAppDataLocator Default implementation for application data folder locator
    %   This class provides platform-specific application data folder paths
    %   for Linux, macOS, and Windows.

    % Copyright 2026 The MathWorks, Inc.

    properties (GetAccess = private, SetAccess = immutable)
        OSFacade(1, 1) mcpserver.internal.facade.os.OSFacade = mcpserver.internal.facade.os.DefaultOSFacade()
    end

    methods
        function obj = DefaultAppDataLocator(options)
            arguments
                options.?mcpserver.internal.appdata.DefaultAppDataLocator
            end

            for prop = string(fieldnames(options).')
                obj.(prop) = options.(prop);
            end
        end

        function path = getAppDataFolder(obj)
            if obj.OSFacade.ismac()
                % macOS
                home = obj.OSFacade.getenv("HOME");
                if home == ""
                    throw(mcpserver.internal.error.Errors.MissingEnvironmentVariable("HOME"));
                end
                appData = fullfile(home, "Library", "Application Support", "MathWorks", "MATLAB MCP Server");
            elseif obj.OSFacade.ispc()
                % Windows
                commonAppData = obj.OSFacade.getenv("APPDATA");
                if commonAppData == ""
                    throw(mcpserver.internal.error.Errors.MissingEnvironmentVariable("APPDATA"));
                end
                appData = fullfile(commonAppData, "MathWorks", "MATLAB MCP Server");
            elseif obj.OSFacade.isunix()
                % Linux/Unix
                home = obj.OSFacade.getenv("HOME");
                if home == ""
                    throw(mcpserver.internal.error.Errors.MissingEnvironmentVariable("HOME"));
                end
                appData = fullfile(home, ".MathWorks", "MATLABMCPServer");
            else
                throw(mcpserver.internal.error.Errors.UnsupportedOS());
            end

            path = appData;
        end
    end

end
