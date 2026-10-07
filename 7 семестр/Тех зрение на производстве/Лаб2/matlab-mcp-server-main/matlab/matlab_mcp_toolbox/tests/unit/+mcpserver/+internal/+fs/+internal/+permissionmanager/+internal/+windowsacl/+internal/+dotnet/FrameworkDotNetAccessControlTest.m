classdef FrameworkDotNetAccessControlTest < matlab.unittest.TestCase
    %FrameworkDotNetAccessControlTest Unit tests for FrameworkDotNetAccessControl

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testFrameworkDotNetAccessControl_SetAccessControl_DelegatesToTarget(testCase)
            % Arrange
            callLog = {};
            mockSecurity = struct(Data="test");
            mockTarget = struct(SetAccessControl=@(s) logCall(s));

            strategy = mcpserver.internal.fs.internal.permissionmanager.internal.windowsacl.internal.dotnet.FrameworkDotNetAccessControl();

            % Act
            strategy.setAccessControl(mockTarget, mockSecurity);

            % Assert
            testCase.verifyEqual(callLog{1}, mockSecurity);

            function logCall(security)
                callLog{end+1} = security;
            end
        end
    end

end
