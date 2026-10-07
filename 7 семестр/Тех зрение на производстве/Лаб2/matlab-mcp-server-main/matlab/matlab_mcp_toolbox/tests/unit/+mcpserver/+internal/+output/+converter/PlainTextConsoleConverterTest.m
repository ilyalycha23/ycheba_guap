classdef PlainTextConsoleConverterTest < matlab.unittest.TestCase
    %PlainTextConsoleConverterTest Unit tests for PlainTextConsoleConverter

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testPlainTextConsoleConverter_Convert_StdoutEvent_ReturnsConsoleOutputStruct(testCase)
            converter = mcpserver.internal.output.converter.PlainTextConsoleConverter();
            evt = struct('type', 'stdout', 'payload', 'hello world');

            result = converter.convert(evt);

            testCase.verifyEqual(result.outputType, 'consoleOutput');
            testCase.verifyEqual(result.text, 'hello world');
        end

        function testPlainTextConsoleConverter_Convert_StderrEvent_ReturnsConsoleOutputStruct(testCase)
            converter = mcpserver.internal.output.converter.PlainTextConsoleConverter();
            evt = struct('type', 'stderr', 'payload', 'error message');

            result = converter.convert(evt);

            testCase.verifyEqual(result.outputType, 'consoleOutput');
            testCase.verifyEqual(result.text, 'error message');
        end

        function testPlainTextConsoleConverter_Convert_StringPayload_ReturnsChar(testCase)
            converter = mcpserver.internal.output.converter.PlainTextConsoleConverter();
            evt = struct('type', 'stdout', 'payload', "string value");

            result = converter.convert(evt);

            testCase.verifyClass(result.text, 'char');
            testCase.verifyEqual(result.text, 'string value');
        end

        function testPlainTextConsoleConverter_Convert_EmptyPayload_ReturnsEmptyChar(testCase)
            converter = mcpserver.internal.output.converter.PlainTextConsoleConverter();
            evt = struct('type', 'stdout', 'payload', '');

            result = converter.convert(evt);

            testCase.verifyEqual(result.text, '');
        end

        function testPlainTextConsoleConverter_Convert_MultilinePayload_PreservesNewlines(testCase)
            converter = mcpserver.internal.output.converter.PlainTextConsoleConverter();
            payload = sprintf('line1\nline2\nline3');
            evt = struct('type', 'stdout', 'payload', payload);

            result = converter.convert(evt);

            testCase.verifyEqual(result.text, payload);
        end
    end

end
