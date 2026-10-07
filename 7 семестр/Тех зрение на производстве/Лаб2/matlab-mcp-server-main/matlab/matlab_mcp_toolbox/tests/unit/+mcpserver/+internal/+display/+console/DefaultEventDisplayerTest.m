classdef DefaultEventDisplayerTest < matlab.unittest.TestCase
    %DefaultEventDisplayerTest Tests for DefaultEventDisplayer

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testDefaultEventDisplayer_IsEventDisplayer(testCase)
            % Arrange & Act
            displayer = mcpserver.internal.display.console.DefaultEventDisplayer();

            % Assert
            testCase.verifyInstanceOf( ...
                displayer, ...
                ?mcpserver.internal.display.console.EventDisplayer, ...
                "DefaultEventDisplayer should be an EventDisplayer" ...
            );
        end

        function testDefaultEventDisplayer_DisplayEvents_Stdout_HappyPath(testCase)
            % Arrange
            displayer = mcpserver.internal.display.console.DefaultEventDisplayer();
            events = struct('type', {'stdout'}, 'payload', {'hello world'});

            % Act
            output = captureDisplay(displayer, events);

            % Assert
            testCase.verifySubstring(output, "hello world", ...
                "Stdout events should be written to standard output" ...
            );
        end

        function testDefaultEventDisplayer_DisplayEvents_Stderr_HappyPath(testCase)
            % Arrange
            displayer = mcpserver.internal.display.console.DefaultEventDisplayer();
            events = struct('type', {'stderr'}, 'payload', {'error msg'});

            % Act
            output = captureDisplay(displayer, events);

            % Assert
            testCase.verifySubstring(output, "error msg", ...
                "Stderr events should render the payload content" ...
            );
        end

        function testDefaultEventDisplayer_DisplayEvents_Stderr_DoesNotError(testCase)
            % Arrange
            displayer = mcpserver.internal.display.console.DefaultEventDisplayer();
            events = struct('type', {'stderr'}, 'payload', {'error msg'});

            % Act & Assert
            testCase.verifyWarningFree( ...
                @() displayer.displayEvents(events), ...
                "Stderr rendering should not produce errors or warnings" ...
            );
        end

        function testDefaultEventDisplayer_DisplayEvents_VariableDisplay_HappyPath(testCase)
            % Arrange
            displayer = mcpserver.internal.display.console.DefaultEventDisplayer();
            events = struct( ...
                'type', {'VariableDisplay'}, ...
                'payload', {struct('name', 'ans', 'value', 42)} ...
            );

            % Act
            output = captureDisplay(displayer, events);

            % Assert
            testCase.verifySubstring(output, "42", ...
                "VariableDisplay events should render the variable value" ...
            );
        end

        function testDefaultEventDisplayer_DisplayEvents_IssuedWarning_HappyPath(testCase)
            % Arrange
            displayer = mcpserver.internal.display.console.DefaultEventDisplayer();
            events = struct( ...
                'type', {'IssuedWarning'}, ...
                'payload', {struct('identifier', 'test:warn', 'message', 'something wrong', 'wasDisabled', false)} ...
            );

            % Act
            output = captureDisplay(displayer, events);

            % Assert
            testCase.verifySubstring(output, "something wrong", ...
                "IssuedWarning events should render the warning message" ...
            );
        end

        function testDefaultEventDisplayer_DisplayEvents_IssuedWarning_NoIdentifier(testCase)
            % Arrange
            displayer = mcpserver.internal.display.console.DefaultEventDisplayer();
            events = struct( ...
                'type', {'IssuedWarning'}, ...
                'payload', {struct('identifier', '', 'message', 'generic warning', 'wasDisabled', false)} ...
            );

            % Act
            output = captureDisplay(displayer, events);

            % Assert
            testCase.verifySubstring(output, "generic warning", ...
                "Warning without identifier should still render" ...
            );
        end

        function testDefaultEventDisplayer_DisplayEvents_IssuedWarning_Disabled_Skipped(testCase)
            % Arrange
            displayer = mcpserver.internal.display.console.DefaultEventDisplayer();
            events = struct( ...
                'type', {'IssuedWarning'}, ...
                'payload', {struct('identifier', 'test:w', 'message', 'disabled', 'wasDisabled', true)} ...
            );

            % Act
            output = captureDisplay(displayer, events);

            % Assert
            testCase.verifyEqual(strtrim(output), '', ...
                "Disabled warnings should be treated as Unknown and skipped" ...
            );
        end

        function testDefaultEventDisplayer_DisplayEvents_Figure_Skipped(testCase)
            % Arrange
            displayer = mcpserver.internal.display.console.DefaultEventDisplayer();
            events = struct('type', {'figure'}, 'payload', {[]});

            % Act
            output = captureDisplay(displayer, events);

            % Assert
            testCase.verifyEqual(strtrim(output), '', ...
                "Figure events should be silently skipped" ...
            );
        end

        function testDefaultEventDisplayer_DisplayEvents_UnknownEvent_Skipped(testCase)
            % Arrange
            displayer = mcpserver.internal.display.console.DefaultEventDisplayer();
            events = struct('type', {'unknownType'}, 'payload', {'data'});

            % Act
            output = captureDisplay(displayer, events);

            % Assert
            testCase.verifyEqual(strtrim(output), '', ...
                "Unknown events should be silently skipped" ...
            );
        end

        function testDefaultEventDisplayer_DisplayEvents_MultipleEvents_RenderedInOrder(testCase)
            % Arrange
            displayer = mcpserver.internal.display.console.DefaultEventDisplayer();
            events = struct( ...
                'type', {'stdout', 'stdout', 'stdout'}, ...
                'payload', {'first', 'second', 'third'} ...
            );

            % Act
            output = captureDisplay(displayer, events);

            % Assert
            firstPos = strfind(output, 'first');
            secondPos = strfind(output, 'second');
            thirdPos = strfind(output, 'third');
            testCase.verifyGreaterThan(secondPos(1), firstPos(1), ...
                "Events should be rendered in order" ...
            );
            testCase.verifyGreaterThan(thirdPos(1), secondPos(1), ...
                "Events should be rendered in order" ...
            );
        end

        function testDefaultEventDisplayer_DisplayEvents_MixedEventTypes_AllRendered(testCase)
            % Arrange
            displayer = mcpserver.internal.display.console.DefaultEventDisplayer();
            events = struct( ...
                'type', {'stdout', 'IssuedWarning', 'stdout'}, ...
                'payload', {'line1', struct('identifier', 'x:y', 'message', 'warn msg', 'wasDisabled', false), 'line2'} ...
            );

            % Act
            output = captureDisplay(displayer, events);

            % Assert
            testCase.verifySubstring(output, "line1", ...
                "Stdout event should be rendered" ...
            );
            testCase.verifySubstring(output, "warn msg", ...
                "Warning event should be rendered" ...
            );
            testCase.verifySubstring(output, "line2", ...
                "Second stdout event should be rendered" ...
            );
        end
    end

end

function output = captureDisplay(displayer, events)
    fcn = @() displayer.displayEvents(events); %#ok<NASGU>
    output = evalc('fcn();');
end
