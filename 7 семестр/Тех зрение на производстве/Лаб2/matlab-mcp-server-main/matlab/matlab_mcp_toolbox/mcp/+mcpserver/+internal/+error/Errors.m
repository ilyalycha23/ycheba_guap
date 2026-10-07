classdef Errors
    %Errors Error catalog for mcpserver
    %   This class provides static methods that return MException objects
    %   for known error conditions.

    % Copyright 2026 The MathWorks, Inc.

    methods (Static)
        function ex = UnsupportedOS()
            %UnsupportedOS Create an error for unsupported operating systems
            ex = MException("mcpserver:UnsupportedOS", ...
                "Unsupported operating system. Operating system must be Windows, Linux, or macOS.");
        end

        function ex = FailedToCreateDirectory(path, msg)
            %FailedToCreateDirectory Create an error for directory creation failure
            ex = MException("mcpserver:FailedToCreateDirectory", ...
                "Failed to create directory '%s': %s", path, msg);
        end

        function ex = FailedToGetFileAttributes(path)
            %FailedToGetFileAttributes Create an error for file attribute retrieval failure
            ex = MException("mcpserver:FailedToGetFileAttributes", ...
                "Failed to get file attributes for '%s'", path);
        end

        function ex = FailedToSetPermissions(path)
            %FailedToSetPermissions Create an error for permission setting failure
            ex = MException("mcpserver:FailedToSetPermissions", ...
                "Failed to set permissions on '%s'", path);
        end

        function ex = InsecurePermissions(path)
            %InsecurePermissions Create an error for insecure permissions
            ex = MException("mcpserver:InsecurePermissions", ...
                "Insecure permissions on '%s': Access must be restricted to the user only.", path);
        end

        function ex = UnsupportedMATLABVersion(featureName, minRelease)
            %UnsupportedMATLABVersion Create an error for unsupported MATLAB version
            ex = MException("mcpserver:UnsupportedMATLABVersion", ...
                "%s requires MATLAB %s or later.", featureName, minRelease);
        end

        function ex = MissingEnvironmentVariable(varName)
            %MissingEnvironmentVariable Create an error for missing environment variable
            ex = MException("mcpserver:MissingEnvironmentVariable", ...
                "Required environment variable '%s' is not set", varName);
        end

        function ex = SecureKeyGenerationFailed()
            %SecureKeyGenerationFailed Create an error for secure key generation failure
            ex = MException("mcpserver:SecureKeyGenerationFailed", ...
                "Failed to generate secure key.");
        end

        function ex = FileExistsAtFolderPath(path)
            %FileExistsAtFolderPath Create an error when a file exists where a folder is expected
            ex = MException("mcpserver:FileExistsAtFolderPath", ...
                "A file already exists at the expected folder path '%s'", path);
        end

        function ex = FolderExistsAtFilePath(path)
            %FolderExistsAtFilePath Create an error when a folder exists where a file is expected
            ex = MException("mcpserver:FolderExistsAtFilePath", ...
                "A folder already exists at the expected file path '%s'", path);
        end

        function ex = FailedToLoadDotNetAssembly(assemblyPath)
            %FailedToLoadDotNetAssembly Create an error for .NET assembly load failure
            ex = MException("mcpserver:FailedToLoadDotNetAssembly", ...
                "Failed to load .NET assembly '%s'. Ensure the .NET runtime is properly installed.", assemblyPath);
        end

        function ex = FailedToReadFile(path)
            %FailedToReadFile Create an error for file read failure
            ex = MException("mcpserver:FailedToReadFile", ...
                "Failed to open file for reading: '%s'", path);
        end
    end

end
