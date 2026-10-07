classdef (Abstract) DotNetFacade
    %DotNetFacade Abstract facade for .NET interop calls
    %   This abstract class defines the interface for .NET system calls
    %   used across the codebase. Enables unit testing by allowing mocks
    %   to replace real .NET calls.

    % Copyright 2026 The MathWorks, Inc.

    methods (Abstract)
        identity = getCurrentWindowsIdentity(obj)
        security = DirectorySecurity(obj, varargin)
        security = FileSecurity(obj, varargin)
        dirInfo = createDirectoryInfo(obj, path)
        fileInfo = createFileInfo(obj, path)
        accessSections = getAccessSectionsAccess(obj)
        accessControlType = getAllowAccessControlType(obj)
        rng = createRandomNumberGenerator(obj)
        bytes = createByteArray(obj, size)
        asm = addAssembly(obj, path)
        runtime = getDotNetRuntime(obj)
        setFileSystemAccessControl(obj, target, security)
    end

end
