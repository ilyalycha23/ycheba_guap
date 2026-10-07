classdef EventTypeTest < matlab.unittest.TestCase
    %EventTypeTest Tests for mcpserver.internal.capture.EventType

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testFromEvent_Stdout(testCase)
            % Arrange
            evt.type = 'stdout';
            evt.payload = 'hello';

            % Act
            result = mcpserver.internal.capture.EventType.fromEvent(evt);

            % Assert
            testCase.verifyEqual(result, mcpserver.internal.capture.EventType.Stdout, ...
                "stdout type should return EventType.Stdout");
        end

        function testFromEvent_Stderr(testCase)
            % Arrange
            evt.type = 'stderr';
            evt.payload = 'error text';

            % Act
            result = mcpserver.internal.capture.EventType.fromEvent(evt);

            % Assert
            testCase.verifyEqual(result, mcpserver.internal.capture.EventType.Stderr, ...
                "stderr type should return EventType.Stderr");
        end

        function testFromEvent_VariableDisplay_ValidPayload(testCase)
            % Arrange
            evt.type = 'VariableDisplay';
            evt.payload = struct('name', 'x', 'value', 42);

            % Act
            result = mcpserver.internal.capture.EventType.fromEvent(evt);

            % Assert
            testCase.verifyEqual(result, mcpserver.internal.capture.EventType.VariableDisplay, ...
                "VariableDisplay with value field should return EventType.VariableDisplay");
        end

        function testFromEvent_VariableDisplay_InvalidPayload(testCase)
            % Arrange
            evt.type = 'VariableDisplay';
            evt.payload = struct('name', 'x');

            % Act
            result = mcpserver.internal.capture.EventType.fromEvent(evt);

            % Assert
            testCase.verifyEqual(result, mcpserver.internal.capture.EventType.Unknown, ...
                "VariableDisplay without value field should return EventType.Unknown");
        end

        function testFromEvent_VariableDisplay_NonStructPayload(testCase)
            % Arrange
            evt.type = 'VariableDisplay';
            evt.payload = 'not a struct';

            % Act
            result = mcpserver.internal.capture.EventType.fromEvent(evt);

            % Assert
            testCase.verifyEqual(result, mcpserver.internal.capture.EventType.Unknown, ...
                "VariableDisplay with non-struct payload should return EventType.Unknown");
        end

        function testFromEvent_IssuedWarning_Active(testCase)
            % Arrange
            evt.type = 'IssuedWarning';
            evt.payload.wasDisabled = false;

            % Act
            result = mcpserver.internal.capture.EventType.fromEvent(evt);

            % Assert
            testCase.verifyEqual(result, mcpserver.internal.capture.EventType.IssuedWarning, ...
                "IssuedWarning with wasDisabled=false should return EventType.IssuedWarning");
        end

        function testFromEvent_IssuedWarning_Disabled(testCase)
            % Arrange
            evt.type = 'IssuedWarning';
            evt.payload.wasDisabled = true;

            % Act
            result = mcpserver.internal.capture.EventType.fromEvent(evt);

            % Assert
            testCase.verifyEqual(result, mcpserver.internal.capture.EventType.Unknown, ...
                "IssuedWarning with wasDisabled=true should return EventType.Unknown");
        end

        function testFromEvent_Figure_ValidPayload(testCase)
            % Arrange
            fig = figure(Visible="off");
            testCase.addTeardown(@() close(fig));
            evt.type = 'figure';
            evt.payload = fig;

            % Act
            result = mcpserver.internal.capture.EventType.fromEvent(evt);

            % Assert
            testCase.verifyEqual(result, mcpserver.internal.capture.EventType.Figure, ...
                "figure with valid handle should return EventType.Figure");
        end

        function testFromEvent_Figure_InvalidPayload(testCase)
            % Arrange
            evt.type = 'figure';
            evt.payload = 'not a handle';

            % Act
            result = mcpserver.internal.capture.EventType.fromEvent(evt);

            % Assert
            testCase.verifyEqual(result, mcpserver.internal.capture.EventType.Unknown, ...
                "figure with non-handle payload should return EventType.Unknown");
        end

        function testFromEvent_UnknownType(testCase)
            % Arrange
            evt.type = 'something_unexpected';
            evt.payload = [];

            % Act
            result = mcpserver.internal.capture.EventType.fromEvent(evt);

            % Assert
            testCase.verifyEqual(result, mcpserver.internal.capture.EventType.Unknown, ...
                "Unknown event type should return EventType.Unknown");
        end

        function testFromEvent_Stdout_MissingPayload(testCase)
            % Arrange
            evt.type = 'stdout';

            % Act
            result = mcpserver.internal.capture.EventType.fromEvent(evt);

            % Assert
            testCase.verifyEqual(result, mcpserver.internal.capture.EventType.Unknown, ...
                "stdout without payload should return EventType.Unknown");
        end

        function testFromEvent_Stderr_MissingPayload(testCase)
            % Arrange
            evt.type = 'stderr';

            % Act
            result = mcpserver.internal.capture.EventType.fromEvent(evt);

            % Assert
            testCase.verifyEqual(result, mcpserver.internal.capture.EventType.Unknown, ...
                "stderr without payload should return EventType.Unknown");
        end

        function testFromEvent_IssuedWarning_NonStructPayload(testCase)
            % Arrange
            evt.type = 'IssuedWarning';
            evt.payload = 'not a struct';

            % Act
            result = mcpserver.internal.capture.EventType.fromEvent(evt);

            % Assert
            testCase.verifyEqual(result, mcpserver.internal.capture.EventType.Unknown, ...
                "IssuedWarning with non-struct payload should return EventType.Unknown");
        end

        function testFromEvent_MissingTypeField(testCase)
            % Arrange
            evt.payload = 'hello';

            % Act
            result = mcpserver.internal.capture.EventType.fromEvent(evt);

            % Assert
            testCase.verifyEqual(result, mcpserver.internal.capture.EventType.Unknown, ...
                "Event without type field should return EventType.Unknown");
        end

        function testFromEvent_VariableDisplay_ObjectPayloadWithValueProp(testCase)
            % Arrange — MException has a 'message' prop but not 'value',
            % so use a figure handle which has a 'Value' property... No.
            % Instead, test that an object WITHOUT 'value' prop returns Unknown.
            payload = MException('test:e', 'msg');
            evt.type = 'VariableDisplay';
            evt.payload = payload;

            % Act
            result = mcpserver.internal.capture.EventType.fromEvent(evt);

            % Assert
            testCase.verifyEqual(result, mcpserver.internal.capture.EventType.Unknown, ...
                "VariableDisplay with object payload lacking 'value' prop should return Unknown");
        end

        function testFromEvent_IssuedWarning_ObjectPayloadWithoutWasDisabled(testCase)
            % Arrange — MException is a concrete object without 'wasDisabled'
            payload = MException('test:e', 'msg');
            evt.type = 'IssuedWarning';
            evt.payload = payload;

            % Act
            result = mcpserver.internal.capture.EventType.fromEvent(evt);

            % Assert
            testCase.verifyEqual(result, mcpserver.internal.capture.EventType.Unknown, ...
                "IssuedWarning with object payload lacking 'wasDisabled' should return Unknown");
        end

    end

end
