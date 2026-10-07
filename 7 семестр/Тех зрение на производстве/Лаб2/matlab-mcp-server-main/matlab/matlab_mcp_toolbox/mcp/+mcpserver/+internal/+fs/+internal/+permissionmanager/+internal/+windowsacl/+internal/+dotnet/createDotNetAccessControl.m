function strategy = createDotNetAccessControl(options)
    %createDotNetAccessControl Factory that selects the correct strategy for the active .NET runtime

    % Copyright 2026 The MathWorks, Inc.

    arguments
        options.OSFacade mcpserver.internal.facade.os.OSFacade = ...
            mcpserver.internal.facade.os.DefaultOSFacade()
        options.DotNetFacade mcpserver.internal.facade.dotnet.DotNetFacade = ...
            mcpserver.internal.facade.dotnet.DefaultDotNetFacade()
    end

    if ~options.OSFacade.ispc()
        strategy = mcpserver.internal.fs.internal.permissionmanager.internal.windowsacl.internal.dotnet.CoreDotNetAccessControl( ...
            DotNetFacade=options.DotNetFacade);
        return;
    end

    runtime = options.DotNetFacade.getDotNetRuntime();
    if runtime == "framework"
        strategy = mcpserver.internal.fs.internal.permissionmanager.internal.windowsacl.internal.dotnet.FrameworkDotNetAccessControl();
    else
        strategy = mcpserver.internal.fs.internal.permissionmanager.internal.windowsacl.internal.dotnet.CoreDotNetAccessControl( ...
            DotNetFacade=options.DotNetFacade);
    end
end
