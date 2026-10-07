function shareMATLABSession(options)
    %shareMATLABSession Share the current MATLAB session via MCP server
    %   This function enables sharing of the MATLAB session through the
    %   Model Context Protocol (MCP) server.

    % Copyright 2026 The MathWorks, Inc.

    arguments
        options.AppDataLocator(1, 1) mcpserver.internal.appdata.AppDataLocator = mcpserver.internal.appdata.DefaultAppDataLocator()
        options.FSAdaptor(1, 1) mcpserver.internal.fs.FSAdaptor = mcpserver.internal.fs.DefaultFSAdaptor()
        options.FSFacade(1, 1) mcpserver.internal.facade.fs.FSFacade = mcpserver.internal.facade.fs.DefaultFSFacade()
        options.ConnectorAdaptor(1, 1) mcpserver.internal.connector.ConnectorAdaptor = mcpserver.internal.connector.DefaultConnectorAdaptor()
        options.ConnectorFacade(1, 1) mcpserver.internal.facade.connector.ConnectorFacade = mcpserver.internal.facade.connector.DefaultConnectorFacade()
    end

    options.ConnectorFacade.ensureServiceOn();

    appDataFolder = options.AppDataLocator.getAppDataFolder();
    options.FSAdaptor.ensureSecureFolder(appDataFolder);

    v1Folder = fullfile(appDataFolder, "v1");
    options.FSAdaptor.ensureSecureFolder(v1Folder);

    sessionDetailsPath = fullfile(v1Folder, "sessionDetails.json");
    options.FSAdaptor.ensureSecureFile(sessionDetailsPath);

    sessionDetails = options.ConnectorAdaptor.getConnectionDetails();
    jsonText = jsonencode(sessionDetails, PrettyPrint=true);
    options.FSFacade.writelines(jsonText, sessionDetailsPath);
end
