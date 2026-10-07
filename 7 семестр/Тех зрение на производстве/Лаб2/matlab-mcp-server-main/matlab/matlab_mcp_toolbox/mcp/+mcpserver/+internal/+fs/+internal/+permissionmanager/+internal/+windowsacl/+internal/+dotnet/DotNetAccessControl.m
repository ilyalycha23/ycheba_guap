classdef (Abstract, HandleCompatible) DotNetAccessControl
    %DotNetAccessControl Abstract interface for .NET runtime-specific ACL operations
    %   Encapsulates differences between .NET Framework and .NET Core
    %   for applying access control to files and directories.

    % Copyright 2026 The MathWorks, Inc.

    methods (Abstract)
        setAccessControl(obj, target, security)
    end

end
