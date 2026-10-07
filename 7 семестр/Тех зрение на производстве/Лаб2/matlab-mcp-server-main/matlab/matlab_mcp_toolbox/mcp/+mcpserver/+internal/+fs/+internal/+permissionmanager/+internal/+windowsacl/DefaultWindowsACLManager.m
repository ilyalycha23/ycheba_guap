classdef DefaultWindowsACLManager < handle & mcpserver.internal.fs.internal.permissionmanager.internal.windowsacl.WindowsACLManager
    %DefaultWindowsACLManager Default implementation using .NET Security APIs
    %   Uses .NET System.Security.AccessControl for Windows ACL operations.
    %   Works entirely with SIDs via SDDL format. All operations run
    %   in-process with no subprocess overhead.
    %
    %   The current user SID is cached (never changes during a MATLAB session).

    % Copyright 2026 The MathWorks, Inc.

    properties (Access = private)
        CachedUserSID string = string.empty
    end

    properties (GetAccess = private, SetAccess = immutable)
        DotNetAccessControl(1, 1) mcpserver.internal.fs.internal.permissionmanager.internal.windowsacl.internal.dotnet.DotNetAccessControl = ...
            mcpserver.internal.fs.internal.permissionmanager.internal.windowsacl.internal.dotnet.createDotNetAccessControl()
        DotNetFacade(1, 1) mcpserver.internal.facade.dotnet.DotNetFacade = ...
            mcpserver.internal.facade.dotnet.DefaultDotNetFacade()
    end

    methods
        function obj = DefaultWindowsACLManager(options)
            arguments
                options.?mcpserver.internal.fs.internal.permissionmanager.internal.windowsacl.DefaultWindowsACLManager
            end

            for prop = string(fieldnames(options).')
                obj.(prop) = options.(prop);
            end
        end

        function sid = getCurrentUserSID(obj)
            %getCurrentUserSID Get the SID of the current process user (cached)
            if ~isempty(obj.CachedUserSID)
                sid = obj.CachedUserSID;
                return;
            end

            identity = obj.DotNetFacade.getCurrentWindowsIdentity();
            obj.CachedUserSID = string(identity.User.ToString());
            sid = obj.CachedUserSID;
        end

        function sids = getAllowedSIDs(obj, path)
            %getAllowedSIDs Get SIDs of all Allow ACEs on a path
            accessSections = obj.DotNetFacade.getAccessSectionsAccess();

            if isfolder(path)
                security = obj.DotNetFacade.DirectorySecurity(char(path), accessSections);
            else
                security = obj.DotNetFacade.FileSecurity(char(path), accessSections);
            end

            identity = obj.DotNetFacade.getCurrentWindowsIdentity();
            sidType = identity.User.GetType();
            rules = security.GetAccessRules(true, true, sidType);

            allowType = obj.DotNetFacade.getAllowAccessControlType();
            sids = strings(1, rules.Count);
            n = 0;
            for i = 0:rules.Count-1
                rule = rules.Item(i);
                if rule.AccessControlType == allowType
                    n = n + 1;
                    sids(n) = string(rule.IdentityReference.ToString());
                end
            end
            sids = sids(1:n);
        end

        function tf = isDACLProtected(obj, path)
            %isDACLProtected Check if the DACL is protected (inheritance blocked)
            accessSections = obj.DotNetFacade.getAccessSectionsAccess();

            if isfolder(path)
                security = obj.DotNetFacade.DirectorySecurity(char(path), accessSections);
            else
                security = obj.DotNetFacade.FileSecurity(char(path), accessSections);
            end

            sddl = string(security.GetSecurityDescriptorSddlForm(accessSections));
            tf = startsWith(sddl, "D:P");
        end

        function setProtectedACL(obj, path, sids, isDirectory)
            %setProtectedACL Set a protected ACL with FullControl for the given SIDs

            % Build SDDL
            sddl = "D:P";
            for i = 1:length(sids)
                if isDirectory
                    sddl = sddl + sprintf("(A;OICI;FA;;;%s)", sids(i));
                else
                    sddl = sddl + sprintf("(A;;FA;;;%s)", sids(i));
                end
            end

            % Apply SDDL to the path
            accessSections = obj.DotNetFacade.getAccessSectionsAccess();
            if isDirectory
                security = obj.DotNetFacade.DirectorySecurity();
                security.SetSecurityDescriptorSddlForm(char(sddl), accessSections);
                dirInfo = obj.DotNetFacade.createDirectoryInfo(path);
                obj.DotNetAccessControl.setAccessControl(dirInfo, security);
            else
                security = obj.DotNetFacade.FileSecurity();
                security.SetSecurityDescriptorSddlForm(char(sddl), accessSections);
                fileInfo = obj.DotNetFacade.createFileInfo(path);
                obj.DotNetAccessControl.setAccessControl(fileInfo, security);
            end
        end
    end

end
