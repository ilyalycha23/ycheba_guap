classdef OutputBuilderTest < matlab.mock.TestCase
    %OutputBuilderTest Unit tests for OutputBuilder

    % Copyright 2026 The MathWorks, Inc.

    methods (Access = private)
        function [mockConverter, converterBehavior] = createMockFigureConverter(testCase)
            import matlab.mock.actions.AssignOutputs

            [mockConverter, converterBehavior] = testCase.createMock( ...
                ?mcpserver.internal.output.converter.Converter, ...
                Strict=true ...
            );

            when( ...
                withAnyInputs(converterBehavior.convert), ...
                AssignOutputs(struct('outputType', 'figure', 'mimeType', 'image/png', 'data', 'fakeB64')) ...
            );
        end
    end

    methods (Test)
        function testOutputBuilder_Build_EmptyEvents_ReturnsEmptyCell(testCase)
            builder = mcpserver.internal.output.OutputBuilder();
            events = struct('type', {}, 'payload', {});

            results = builder.build(events);

            testCase.verifyEmpty(results);
        end

        function testOutputBuilder_Build_StdoutEvent_ReturnsTextStruct(testCase)
            builder = mcpserver.internal.output.OutputBuilder();
            events = struct('type', {'stdout'}, 'payload', {'hello world'});

            results = builder.build(events);

            testCase.verifyLength(results, 1);
            testCase.verifyEqual(results{1}.outputType, 'consoleOutput');
            testCase.verifyEqual(results{1}.text, 'hello world');
        end

        function testOutputBuilder_Build_MultipleStdoutEvents_SeparateItems(testCase)
            builder = mcpserver.internal.output.OutputBuilder();
            events = struct( ...
                'type', {'stdout', 'stdout'}, ...
                'payload', {'hello ', 'world'} ...
            );

            results = builder.build(events);

            testCase.verifyLength(results, 2);
            testCase.verifyEqual(results{1}.text, 'hello ');
            testCase.verifyEqual(results{2}.text, 'world');
        end

        function testOutputBuilder_Build_StderrEvent_ReturnsTextStruct(testCase)
            builder = mcpserver.internal.output.OutputBuilder();
            events = struct('type', {'stderr'}, 'payload', {'error msg'});

            results = builder.build(events);

            testCase.verifyLength(results, 1);
            testCase.verifyEqual(results{1}.outputType, 'consoleOutput');
            testCase.verifyEqual(results{1}.text, 'error msg');
        end

        function testOutputBuilder_Build_FigureEvent_RoutesToConverter(testCase)
            [mockConverter, converterBehavior] = testCase.createMockFigureConverter();
            builder = mcpserver.internal.output.OutputBuilder(FigureConverter=mockConverter);
            events = struct('type', {'figure'}, 'payload', {0});

            results = builder.build(events);

            testCase.verifyLength(results, 1);
            testCase.verifyEqual(results{1}.outputType, 'figure');
            testCase.verifyEqual(results{1}.mimeType, 'image/png');
            testCase.verifyEqual(results{1}.data, 'fakeB64');
            testCase.verifyCalled( ...
                withAnyInputs(converterBehavior.convert), ...
                "convert should be called with the event" ...
            );
        end

        function testOutputBuilder_Build_MixedEvents_CorrectOrdering(testCase)
            [mockConverter, ~] = testCase.createMockFigureConverter();
            builder = mcpserver.internal.output.OutputBuilder(FigureConverter=mockConverter);
            events = struct( ...
                'type', {'stdout', 'figure', 'stdout'}, ...
                'payload', {'before', 0, 'after'} ...
            );

            results = builder.build(events);

            testCase.verifyLength(results, 3);
            testCase.verifyEqual(results{1}.text, 'before');
            testCase.verifyEqual(results{2}.mimeType, 'image/png');
            testCase.verifyEqual(results{3}.text, 'after');
        end

        function testOutputBuilder_Build_WarningEvent_ReturnsWarningStruct(testCase)
            builder = mcpserver.internal.output.OutputBuilder();
            payload = struct('message', 'something went wrong', 'identifier', 'test:warn', 'wasDisabled', false);
            events = struct('type', {'IssuedWarning'}, 'payload', {payload});

            results = builder.build(events);

            testCase.verifyLength(results, 1);
            testCase.verifyEqual(results{1}.outputType, 'warning');
            testCase.verifyEqual(results{1}.text, 'something went wrong');
            testCase.verifyEqual(results{1}.identifier, 'test:warn');
        end

        function testOutputBuilder_Build_UnknownEvent_SkippedSilently(testCase)
            builder = mcpserver.internal.output.OutputBuilder();
            events = struct('type', {'unknownType'}, 'payload', {'ignored'});

            results = builder.build(events);

            testCase.verifyEmpty(results);
        end

        function testOutputBuilder_Build_VariableDisplayEvent_RoutesToConverter(testCase)
            import matlab.mock.actions.AssignOutputs

            [mockConverter, converterBehavior] = testCase.createMock( ...
                ?mcpserver.internal.output.converter.Converter, ...
                Strict=true ...
            );

            when( ...
                withAnyInputs(converterBehavior.convert), ...
                AssignOutputs(struct('outputType', 'variable', 'name', 'x', 'text', '42')) ...
            );

            builder = mcpserver.internal.output.OutputBuilder(VariableDisplayConverter=mockConverter);
            payload = struct('name', 'x', 'value', 42);
            events = struct('type', {'VariableDisplay'}, 'payload', {payload});

            results = builder.build(events);

            testCase.verifyLength(results, 1);
            testCase.verifyEqual(results{1}.outputType, 'variable');
            testCase.verifyEqual(results{1}.name, 'x');
            testCase.verifyCalled( ...
                withAnyInputs(converterBehavior.convert), ...
                "convert should be called for VariableDisplay events" ...
            );
        end
    end

end
