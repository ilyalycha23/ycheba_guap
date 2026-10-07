classdef DefaultFigureVisibilityControllerFunctionalTest < matlab.unittest.TestCase
    %DefaultFigureVisibilityControllerFunctionalTest Functional tests for figure visibility control
    %   These tests exercise DefaultFigureVisibilityController with real
    %   MATLAB figures and uifigures to verify visibility toggling and
    %   listener cleanup behavior end-to-end.

    % Copyright 2026 The MathWorks, Inc.

    methods (TestMethodSetup)
        function saveAndRestoreGlobalState(testCase)
            originalVisible = get(0, "DefaultFigureVisible");
            originalCreateFcn = get(0, "DefaultFigureCreateFcn");
            testCase.addTeardown(@() set(0, "DefaultFigureVisible", originalVisible));
            testCase.addTeardown(@() set(0, "DefaultFigureCreateFcn", originalCreateFcn));
            set(0, "DefaultFigureVisible", "on");
            set(0, "DefaultFigureCreateFcn", "");
        end
    end

    methods (Test)
        function testHide_FigureCreatedWhileHidden_IsInvisible(testCase)
            % Arrange
            controller = mcpserver.internal.display.DefaultFigureVisibilityController();
            testCase.addTeardown(@() controller.restore());
            controller.hide();

            % Act
            fig = figure();
            testCase.addTeardown(@() close(fig));

            % Assert
            testCase.verifyEqual( ...
                string(fig.Visible), "off", ...
                "Figure created while hidden should be invisible" ...
            );
        end

        function testShow_FigureCreatedAfterShow_IsVisible(testCase)
            % Arrange
            controller = mcpserver.internal.display.DefaultFigureVisibilityController();
            testCase.addTeardown(@() controller.restore());
            controller.hide();
            controller.show();

            % Act
            fig = figure();
            testCase.addTeardown(@() close(fig));

            % Assert
            testCase.verifyEqual( ...
                string(fig.Visible), "on", ...
                "Figure created after show() should be visible" ...
            );
        end

        function testHide_FigureVisibilityCannotBeToggledOn(testCase)
            % Arrange
            controller = mcpserver.internal.display.DefaultFigureVisibilityController();
            testCase.addTeardown(@() controller.restore());
            controller.hide();

            fig = figure();
            testCase.addTeardown(@() close(fig));

            % Act — attempt to make figure visible while hidden
            fig.Visible = "on";

            % Assert — listener should lock it back to off
            testCase.verifyEqual( ...
                string(fig.Visible), "off", ...
                "Figure visibility should be locked to 'off' by the listener" ...
            );
        end

        function testRestore_AfterHide_FigureVisibilityCanBeToggledOn(testCase)
            % Arrange
            controller = mcpserver.internal.display.DefaultFigureVisibilityController();
            testCase.addTeardown(@() controller.restore());

            controller.hide();
            fig = figure();
            testCase.addTeardown(@() close(fig));
            controller.restore();

            % Act — toggle visibility after restore
            fig.Visible = "on";

            % Assert — listener should have been removed, so it stays on
            testCase.verifyEqual( ...
                string(fig.Visible), "on", ...
                "Figure visibility should be toggleable after restore() clears listeners" ...
            );
        end

        function testShow_AfterHide_FigureVisibilityCanBeToggledOn(testCase)
            % Arrange
            controller = mcpserver.internal.display.DefaultFigureVisibilityController();
            testCase.addTeardown(@() controller.restore());

            controller.hide();
            fig = figure();
            testCase.addTeardown(@() close(fig));
            controller.show();

            % Act — toggle visibility after show
            fig.Visible = "on";

            % Assert — listener should have been removed, so it stays on
            testCase.verifyEqual( ...
                string(fig.Visible), "on", ...
                "Figure visibility should be toggleable after show() clears listeners" ...
            );
        end

        function testRestore_RestoresOriginalDefaultFigureVisible(testCase)
            % Arrange
            originalVisible = get(0, "DefaultFigureVisible");
            controller = mcpserver.internal.display.DefaultFigureVisibilityController();
            testCase.addTeardown(@() controller.restore());
            controller.hide();

            % Act
            controller.restore();

            % Assert
            testCase.verifyEqual( ...
                get(0, "DefaultFigureVisible"), originalVisible, ...
                "DefaultFigureVisible should be restored to its original value" ...
            );
        end

        function testHideThenShowThenRestore_RestoresOriginalState(testCase)
            % Arrange — set a non-default initial state so restore() must
            % actually change something rather than matching show()'s state.
            set(0, "DefaultFigureVisible", "off");
            customCreateFcn = @(~,~) disp("custom");
            set(0, "DefaultFigureCreateFcn", customCreateFcn);

            controller = mcpserver.internal.display.DefaultFigureVisibilityController();
            testCase.addTeardown(@() controller.restore());
            controller.hide();
            controller.show();

            % Act
            controller.restore();

            % Assert
            testCase.verifyEqual( ...
                string(get(0, "DefaultFigureVisible")), "off", ...
                "DefaultFigureVisible should be restored to the original state, not the state after show()" ...
            );
            testCase.verifyEqual( ...
                get(0, "DefaultFigureCreateFcn"), customCreateFcn, ...
                "DefaultFigureCreateFcn should be restored to the original state" ...
            );
        end

        function testHide_UifigureCreatedWhileHidden_IsInvisible(testCase)
            % Arrange
            controller = mcpserver.internal.display.DefaultFigureVisibilityController();
            testCase.addTeardown(@() controller.restore());
            controller.hide();

            % Act
            fig = uifigure();
            testCase.addTeardown(@() close(fig));

            % Assert
            testCase.verifyEqual( ...
                string(fig.Visible), "off", ...
                "Uifigure created while hidden should be invisible" ...
            );
        end

        function testShow_UifigureCreatedAfterShow_IsVisible(testCase)
            % Arrange
            controller = mcpserver.internal.display.DefaultFigureVisibilityController();
            testCase.addTeardown(@() controller.restore());
            controller.hide();
            controller.show();

            % Act
            fig = uifigure();
            testCase.addTeardown(@() close(fig));

            % Assert
            testCase.verifyEqual( ...
                string(fig.Visible), "on", ...
                "Uifigure created after show() should be visible" ...
            );
        end

        function testRestore_AfterHide_NewFiguresAreVisible(testCase)
            % Arrange
            controller = mcpserver.internal.display.DefaultFigureVisibilityController();
            testCase.addTeardown(@() controller.restore());
            controller.hide();

            % Act
            controller.restore();
            fig = figure();
            testCase.addTeardown(@() close(fig));

            % Assert
            testCase.verifyEqual( ...
                string(fig.Visible), "on", ...
                "Figures created after restore() should be visible" ...
            );
        end

        function testRestore_AfterHide_ClosedFigureDoesNotError(testCase)
            % Arrange
            controller = mcpserver.internal.display.DefaultFigureVisibilityController();
            testCase.addTeardown(@() controller.restore());
            controller.hide();

            fig = figure();
            close(fig);

            % Act & Assert — should not error
            testCase.verifyWarningFree( ...
                @() controller.restore(), ...
                "restore() should not error when a locked figure was already closed" ...
            );
        end
    end

end
