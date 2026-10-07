classdef DefaultWindowsACLManagerTest < matlab.unittest.TestCase
%DefaultWindowsACLManagerTest Integration tests for DefaultWindowsACLManager
%   These tests verify the real .NET Security API interactions on Windows.
%   They require a Windows OS with .NET runtime and make actual ACL changes.

    % Copyright 2026 The MathWorks, Inc.

    properties
        TestFolder
    end

    methods (TestClassSetup)
        function checkPlatform(testCase)
            testCase.assumeTrue(ispc(), "Test requires Windows");
        end
    end

    methods (TestMethodSetup)
        function setupTempFolder(testCase)
            tempFixture = testCase.applyFixture( ...
                matlab.unittest.fixtures.TemporaryFolderFixture ...
            );
            testCase.TestFolder = tempFixture.Folder;
        end
    end

    methods (Test)
        function testDefaultWindowsACLManager_GetCurrentUserSID_ReturnsValidWindowsSID(testCase)
            % Arrange
            manager = mcpserver.internal.fs.internal.permissionmanager.internal.windowsacl.DefaultWindowsACLManager();

            % Act
            sid = manager.getCurrentUserSID();

            % Assert
            testCase.verifyTrue(startsWith(sid, "S-1-5-"), ...
                "SID should be a valid Windows SID starting with S-1-5-");
        end

        function testDefaultWindowsACLManager_SetProtectedACL_Directory(testCase)
            % Arrange
            manager = mcpserver.internal.fs.internal.permissionmanager.internal.windowsacl.DefaultWindowsACLManager();
            userSid = manager.getCurrentUserSID();
            sddlSids = [userSid, "SY", "BA"];
            expectedSids = [userSid, "S-1-5-18", "S-1-5-32-544"];

            % Act
            manager.setProtectedACL(testCase.TestFolder, sddlSids, true);

            % Assert
            testCase.verifyTrue(manager.isDACLProtected(testCase.TestFolder), ...
                "DACL should be protected after setProtectedACL");
            allowedSids = manager.getAllowedSIDs(testCase.TestFolder);
            testCase.verifyEqual(sort(allowedSids), sort(expectedSids), ...
                "Only the specified SIDs should have access");
        end

        function testDefaultWindowsACLManager_SetProtectedACL_File(testCase)
            % Arrange
            manager = mcpserver.internal.fs.internal.permissionmanager.internal.windowsacl.DefaultWindowsACLManager();
            userSid = manager.getCurrentUserSID();
            sddlSids = [userSid, "SY", "BA"];
            expectedSids = [userSid, "S-1-5-18", "S-1-5-32-544"];
            testFile = fullfile(testCase.TestFolder, "test.txt");
            writelines("test content", testFile);

            % Act
            manager.setProtectedACL(testFile, sddlSids, false);

            % Assert
            testCase.verifyTrue(manager.isDACLProtected(testFile), ...
                "DACL should be protected after setProtectedACL");
            allowedSids = manager.getAllowedSIDs(testFile);
            testCase.verifyEqual(sort(allowedSids), sort(expectedSids), ...
                "Only the specified SIDs should have access");
        end

        function testDefaultWindowsACLManager_SetProtectedACL_Directory_ChildInheritsACL(testCase)
            % Arrange
            manager = mcpserver.internal.fs.internal.permissionmanager.internal.windowsacl.DefaultWindowsACLManager();
            userSid = manager.getCurrentUserSID();
            sddlSids = [userSid, "SY", "BA"];
            expectedSids = [userSid, "S-1-5-18", "S-1-5-32-544"];

            manager.setProtectedACL(testCase.TestFolder, sddlSids, true);

            % Act
            childFile = fullfile(testCase.TestFolder, "child.txt");
            writelines("test content", childFile);

            % Assert
            childSids = manager.getAllowedSIDs(childFile);
            testCase.verifyEqual(sort(childSids), sort(expectedSids), ...
                "Child file should inherit the parent folder's SIDs via OICI inheritance");
        end

        function testDefaultWindowsACLManager_SetProtectedACL_SingleSID(testCase)
            % Arrange
            manager = mcpserver.internal.fs.internal.permissionmanager.internal.windowsacl.DefaultWindowsACLManager();
            userSid = manager.getCurrentUserSID();

            % Act
            manager.setProtectedACL(testCase.TestFolder, userSid, true);

            % Assert
            testCase.verifyTrue(manager.isDACLProtected(testCase.TestFolder), ...
                "DACL should be protected after setProtectedACL");
            allowedSids = manager.getAllowedSIDs(testCase.TestFolder);
            testCase.verifyEqual(allowedSids, userSid, ...
                "Only the current user SID should have access");
        end
    end

end
