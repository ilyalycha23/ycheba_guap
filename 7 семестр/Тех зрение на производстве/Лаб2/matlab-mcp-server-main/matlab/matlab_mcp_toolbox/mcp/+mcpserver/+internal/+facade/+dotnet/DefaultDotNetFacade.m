classdef DefaultDotNetFacade < mcpserver.internal.facade.dotnet.DotNetFacade
    %DefaultDotNetFacade Default implementation delegating to real .NET calls

    % Copyright 2026 The MathWorks, Inc.

    methods
        function identity = getCurrentWindowsIdentity(~)
            identity = System.Security.Principal.WindowsIdentity.GetCurrent();
        end

        function security = DirectorySecurity(~, varargin)
            security = System.Security.AccessControl.DirectorySecurity(varargin{:});
        end

        function security = FileSecurity(~, varargin)
            security = System.Security.AccessControl.FileSecurity(varargin{:});
        end

        function dirInfo = createDirectoryInfo(~, path)
            dirInfo = System.IO.DirectoryInfo(char(path));
        end

        function fileInfo = createFileInfo(~, path)
            fileInfo = System.IO.FileInfo(char(path));
        end

        function accessSections = getAccessSectionsAccess(~)
            accessSections = System.Security.AccessControl.AccessControlSections.Access;
        end

        function accessControlType = getAllowAccessControlType(~)
            accessControlType = System.Security.AccessControl.AccessControlType.Allow;
        end

        function rng = createRandomNumberGenerator(~)
            rng = System.Security.Cryptography.RandomNumberGenerator.Create();
        end

        function bytes = createByteArray(~, size)
            bytes = NET.createArray('System.Byte', size);
        end

        function asm = addAssembly(~, path)
            asm = NET.addAssembly(char(path));
        end

        function runtime = getDotNetRuntime(~)
            env = dotnetenv();
            runtime = string(env.Runtime);
        end

        function setFileSystemAccessControl(~, target, security)
            System.IO.FileSystemAclExtensions.SetAccessControl(target, security);
        end
    end

end
