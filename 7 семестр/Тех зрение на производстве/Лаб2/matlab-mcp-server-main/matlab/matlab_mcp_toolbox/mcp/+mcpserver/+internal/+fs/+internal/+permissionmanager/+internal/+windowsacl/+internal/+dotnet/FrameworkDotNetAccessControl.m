classdef FrameworkDotNetAccessControl < mcpserver.internal.fs.internal.permissionmanager.internal.windowsacl.internal.dotnet.DotNetAccessControl
    %FrameworkDotNetAccessControl .NET Framework implementation
    %   Uses instance methods on DirectoryInfo/FileInfo which are
    %   available in .NET Framework.

    % Copyright 2026 The MathWorks, Inc.

    methods
        function setAccessControl(~, target, security)
            target.SetAccessControl(security);
        end
    end

end
