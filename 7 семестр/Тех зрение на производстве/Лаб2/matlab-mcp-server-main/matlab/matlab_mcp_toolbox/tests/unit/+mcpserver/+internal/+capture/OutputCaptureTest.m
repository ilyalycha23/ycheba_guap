classdef OutputCaptureTest < matlab.mock.TestCase
    %OutputCaptureTest Tests for mcpserver.internal.capture.DefaultOutputCapture

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testOutputCapture_Enable_CallsFacadeInOrder(testCase)
            % Arrange
            import matlab.mock.actions.AssignOutputs
            import matlab.mock.actions.DoNothing

            [mockFacade, behavior] = testCase.createMock( ...
                ?mcpserver.internal.facade.capture.OutputCaptureFacade, ...
                Strict=true ...
            );

            when(behavior.getAllowOutputCapture().withExactInputs(), AssignOutputs(false));
            when(behavior.getSuppressCommandLineOutput().withExactInputs(), AssignOutputs(false));
            when(behavior.getHotlinks().withExactInputs(), AssignOutputs(true));
            when(behavior.pushTextOutputListeners().withExactInputs(), DoNothing);
            when(behavior.resetStructuredFigures().withExactInputs(), DoNothing);
            when(withAnyInputs(behavior.setAllowOutputCapture), DoNothing);
            when(withAnyInputs(behavior.setSuppressCommandLineOutput), DoNothing);
            when(withAnyInputs(behavior.setHotlinks), DoNothing);
            when(behavior.popTextOutputListeners().withExactInputs(), DoNothing);

            capture = mcpserver.internal.capture.DefaultOutputCapture(Facade=mockFacade);

            % Act
            capture.enable();

            % Assert
            testCase.verifyCalled( ...
                behavior.getAllowOutputCapture().withExactInputs(), ...
                "getAllowOutputCapture should be called to save original state" ...
            );
            testCase.verifyCalled( ...
                behavior.getSuppressCommandLineOutput().withExactInputs(), ...
                "getSuppressCommandLineOutput should be called to save original state" ...
            );
            testCase.verifyCalled( ...
                behavior.getHotlinks().withExactInputs(), ...
                "getHotlinks should be called to save original state" ...
            );
            testCase.verifyCalled( ...
                behavior.pushTextOutputListeners().withExactInputs(), ...
                "pushTextOutputListeners should be called" ...
            );
            testCase.verifyCalled( ...
                behavior.resetStructuredFigures().withExactInputs(), ...
                "resetStructuredFigures should be called" ...
            );
            testCase.verifyCalled( ...
                behavior.setAllowOutputCapture(true), ...
                "setAllowOutputCapture should be called with true" ...
            );
            testCase.verifyCalled( ...
                behavior.setSuppressCommandLineOutput(true), ...
                "setSuppressCommandLineOutput should be called with true" ...
            );
            testCase.verifyCalled( ...
                behavior.setHotlinks(false), ...
                "setHotlinks should be called with false" ...
            );
        end

        function testOutputCapture_Enable_AlreadyEnabled_IsNoOp(testCase)
            % Arrange
            import matlab.mock.actions.AssignOutputs
            import matlab.mock.actions.DoNothing

            [mockFacade, behavior] = testCase.createMock( ...
                ?mcpserver.internal.facade.capture.OutputCaptureFacade, ...
                Strict=true ...
            );

            when(behavior.getAllowOutputCapture().withExactInputs(), AssignOutputs(false));
            when(behavior.getSuppressCommandLineOutput().withExactInputs(), AssignOutputs(false));
            when(behavior.getHotlinks().withExactInputs(), AssignOutputs(true));
            when(behavior.pushTextOutputListeners().withExactInputs(), DoNothing);
            when(behavior.resetStructuredFigures().withExactInputs(), DoNothing);
            when(withAnyInputs(behavior.setAllowOutputCapture), DoNothing);
            when(withAnyInputs(behavior.setSuppressCommandLineOutput), DoNothing);
            when(withAnyInputs(behavior.setHotlinks), DoNothing);
            when(behavior.popTextOutputListeners().withExactInputs(), DoNothing);

            capture = mcpserver.internal.capture.DefaultOutputCapture(Facade=mockFacade);
            capture.enable();

            testCase.clearMockHistory(mockFacade);

            % Act
            capture.enable();

            % Assert
            testCase.verifyNotCalled( ...
                behavior.pushTextOutputListeners().withExactInputs(), ...
                "pushTextOutputListeners should not be called on second enable()" ...
            );
        end

        function testOutputCapture_Disable_RestoresOriginalState(testCase)
            % Arrange
            import matlab.mock.actions.AssignOutputs
            import matlab.mock.actions.DoNothing

            [mockFacade, behavior] = testCase.createMock( ...
                ?mcpserver.internal.facade.capture.OutputCaptureFacade, ...
                Strict=true ...
            );

            originalAllow = true;
            originalSuppress = false;
            originalHotlinks = true;

            when(behavior.getAllowOutputCapture().withExactInputs(), AssignOutputs(originalAllow));
            when(behavior.getSuppressCommandLineOutput().withExactInputs(), AssignOutputs(originalSuppress));
            when(behavior.getHotlinks().withExactInputs(), AssignOutputs(originalHotlinks));
            when(behavior.pushTextOutputListeners().withExactInputs(), DoNothing);
            when(behavior.resetStructuredFigures().withExactInputs(), DoNothing);
            when(withAnyInputs(behavior.setAllowOutputCapture), DoNothing);
            when(withAnyInputs(behavior.setSuppressCommandLineOutput), DoNothing);
            when(withAnyInputs(behavior.setHotlinks), DoNothing);
            when(behavior.popTextOutputListeners().withExactInputs(), DoNothing);

            capture = mcpserver.internal.capture.DefaultOutputCapture(Facade=mockFacade);
            capture.enable();
            testCase.clearMockHistory(mockFacade);

            % Act
            capture.disable();

            % Assert
            testCase.verifyCalled( ...
                behavior.popTextOutputListeners().withExactInputs(), ...
                "popTextOutputListeners should be called" ...
            );
            testCase.verifyCalled( ...
                behavior.setAllowOutputCapture(originalAllow), ...
                "setAllowOutputCapture should restore original value" ...
            );
            testCase.verifyCalled( ...
                behavior.setSuppressCommandLineOutput(originalSuppress), ...
                "setSuppressCommandLineOutput should restore original value" ...
            );
            testCase.verifyCalled( ...
                behavior.setHotlinks(originalHotlinks), ...
                "setHotlinks should restore original value" ...
            );
        end

        function testOutputCapture_Disable_NotEnabled_IsNoOp(testCase)
            % Arrange
            [mockFacade, behavior] = testCase.createMock( ...
                ?mcpserver.internal.facade.capture.OutputCaptureFacade, ...
                Strict=true ...
            );

            capture = mcpserver.internal.capture.DefaultOutputCapture(Facade=mockFacade);

            % Act
            capture.disable();

            % Assert
            testCase.verifyNotCalled( ...
                behavior.popTextOutputListeners().withExactInputs(), ...
                "popTextOutputListeners should not be called when not enabled" ...
            );
        end

        function testOutputCapture_Delete_DisablesCapture(testCase)
            % Arrange
            import matlab.mock.actions.AssignOutputs
            import matlab.mock.actions.DoNothing

            [mockFacade, behavior] = testCase.createMock( ...
                ?mcpserver.internal.facade.capture.OutputCaptureFacade, ...
                Strict=true ...
            );

            when(behavior.getAllowOutputCapture().withExactInputs(), AssignOutputs(false));
            when(behavior.getSuppressCommandLineOutput().withExactInputs(), AssignOutputs(false));
            when(behavior.getHotlinks().withExactInputs(), AssignOutputs(true));
            when(behavior.pushTextOutputListeners().withExactInputs(), DoNothing);
            when(behavior.resetStructuredFigures().withExactInputs(), DoNothing);
            when(withAnyInputs(behavior.setAllowOutputCapture), DoNothing);
            when(withAnyInputs(behavior.setSuppressCommandLineOutput), DoNothing);
            when(withAnyInputs(behavior.setHotlinks), DoNothing);
            when(behavior.popTextOutputListeners().withExactInputs(), DoNothing);

            capture = mcpserver.internal.capture.DefaultOutputCapture(Facade=mockFacade);
            capture.enable();
            testCase.clearMockHistory(mockFacade);

            % Act
            delete(capture);

            % Assert
            testCase.verifyCalled( ...
                behavior.popTextOutputListeners().withExactInputs(), ...
                "delete should trigger disable which calls popTextOutputListeners" ...
            );
        end

        function testOutputCapture_RunUncaptured_WhenEnabled_DisablesAndReenables(testCase)
            % Arrange
            import matlab.mock.actions.AssignOutputs
            import matlab.mock.actions.DoNothing

            [mockFacade, behavior] = testCase.createMock( ...
                ?mcpserver.internal.facade.capture.OutputCaptureFacade, ...
                Strict=true ...
            );

            when(behavior.getAllowOutputCapture().withExactInputs(), AssignOutputs(false));
            when(behavior.getSuppressCommandLineOutput().withExactInputs(), AssignOutputs(false));
            when(behavior.getHotlinks().withExactInputs(), AssignOutputs(true));
            when(behavior.pushTextOutputListeners().withExactInputs(), DoNothing);
            when(behavior.resetStructuredFigures().withExactInputs(), DoNothing);
            when(withAnyInputs(behavior.setAllowOutputCapture), DoNothing);
            when(withAnyInputs(behavior.setSuppressCommandLineOutput), DoNothing);
            when(withAnyInputs(behavior.setHotlinks), DoNothing);
            when(behavior.popTextOutputListeners().withExactInputs(), DoNothing);

            capture = mcpserver.internal.capture.DefaultOutputCapture(Facade=mockFacade);
            capture.enable();
            testCase.clearMockHistory(mockFacade);

            callbackExecuted = false;

            % Act
            capture.runUncaptured(@() setExecuted());

            % Assert
            testCase.verifyCalled( ...
                behavior.popTextOutputListeners().withExactInputs(), ...
                "runUncaptured should disable capture (pop listeners)" ...
            );
            testCase.verifyCalled( ...
                behavior.pushTextOutputListeners().withExactInputs(), ...
                "runUncaptured should re-enable capture (push listeners)" ...
            );
            testCase.verifyTrue(callbackExecuted, ...
                "The callback function should have been executed" ...
            );

            function setExecuted()
                callbackExecuted = true;
            end
        end

        function testOutputCapture_RunUncaptured_WhenNotEnabled_RunsDirectly(testCase)
            % Arrange
            [mockFacade, behavior] = testCase.createMock( ...
                ?mcpserver.internal.facade.capture.OutputCaptureFacade, ...
                Strict=true ...
            );

            capture = mcpserver.internal.capture.DefaultOutputCapture(Facade=mockFacade);

            callbackExecuted = false;

            % Act
            capture.runUncaptured(@() setExecuted());

            % Assert
            testCase.verifyNotCalled( ...
                behavior.popTextOutputListeners().withExactInputs(), ...
                "runUncaptured should not call disable when not enabled" ...
            );
            testCase.verifyTrue(callbackExecuted, ...
                "The callback function should still execute when not enabled" ...
            );

            function setExecuted()
                callbackExecuted = true;
            end
        end

        function testOutputCapture_RunUncaptured_WhenCallbackErrors_StillReenables(testCase)
            % Arrange
            import matlab.mock.actions.AssignOutputs
            import matlab.mock.actions.DoNothing

            [mockFacade, behavior] = testCase.createMock( ...
                ?mcpserver.internal.facade.capture.OutputCaptureFacade, ...
                Strict=true ...
            );

            when(behavior.getAllowOutputCapture().withExactInputs(), AssignOutputs(false));
            when(behavior.getSuppressCommandLineOutput().withExactInputs(), AssignOutputs(false));
            when(behavior.getHotlinks().withExactInputs(), AssignOutputs(true));
            when(behavior.pushTextOutputListeners().withExactInputs(), DoNothing);
            when(behavior.resetStructuredFigures().withExactInputs(), DoNothing);
            when(withAnyInputs(behavior.setAllowOutputCapture), DoNothing);
            when(withAnyInputs(behavior.setSuppressCommandLineOutput), DoNothing);
            when(withAnyInputs(behavior.setHotlinks), DoNothing);
            when(behavior.popTextOutputListeners().withExactInputs(), DoNothing);

            capture = mcpserver.internal.capture.DefaultOutputCapture(Facade=mockFacade);
            capture.enable();
            testCase.clearMockHistory(mockFacade);

            % Act
            try
                capture.runUncaptured(@() error('test:e', 'boom'));
            catch
            end

            % Assert
            testCase.verifyCalled( ...
                behavior.pushTextOutputListeners().withExactInputs(), ...
                "runUncaptured should re-enable capture even when callback errors" ...
            );
        end

        function testOutputCapture_Delete_NotEnabled_IsNoOp(testCase)
            % Arrange
            [mockFacade, behavior] = testCase.createMock( ...
                ?mcpserver.internal.facade.capture.OutputCaptureFacade, ...
                Strict=true ...
            );

            capture = mcpserver.internal.capture.DefaultOutputCapture(Facade=mockFacade);

            % Act
            delete(capture);

            % Assert
            testCase.verifyNotCalled( ...
                behavior.popTextOutputListeners().withExactInputs(), ...
                "delete should not call popTextOutputListeners when not enabled" ...
            );
        end

        function testOutputCapture_RunUncaptured_WhenCallbackErrors_RethrowsError(testCase)
            % Arrange
            import matlab.mock.actions.AssignOutputs
            import matlab.mock.actions.DoNothing

            [mockFacade, behavior] = testCase.createMock( ...
                ?mcpserver.internal.facade.capture.OutputCaptureFacade, ...
                Strict=true ...
            );

            when(behavior.getAllowOutputCapture().withExactInputs(), AssignOutputs(false));
            when(behavior.getSuppressCommandLineOutput().withExactInputs(), AssignOutputs(false));
            when(behavior.getHotlinks().withExactInputs(), AssignOutputs(true));
            when(behavior.pushTextOutputListeners().withExactInputs(), DoNothing);
            when(behavior.resetStructuredFigures().withExactInputs(), DoNothing);
            when(withAnyInputs(behavior.setAllowOutputCapture), DoNothing);
            when(withAnyInputs(behavior.setSuppressCommandLineOutput), DoNothing);
            when(withAnyInputs(behavior.setHotlinks), DoNothing);
            when(behavior.popTextOutputListeners().withExactInputs(), DoNothing);

            capture = mcpserver.internal.capture.DefaultOutputCapture(Facade=mockFacade);
            capture.enable();

            % Act
            thrownError = [];
            try
                capture.runUncaptured(@() error('test:e', 'boom'));
            catch ME
                thrownError = ME;
            end

            % Assert
            testCase.verifyNotEmpty(thrownError, ...
                "runUncaptured should rethrow callback errors");
            testCase.verifyEqual(thrownError.identifier, 'test:e', ...
                "rethrown error should preserve the original identifier");
        end
    end

end
