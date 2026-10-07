classdef PlainTextWarningConverterTest < matlab.unittest.TestCase
    %PlainTextWarningConverterTest Unit tests for PlainTextWarningConverter

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testPlainTextWarningConverter_Convert_HappyPath_ReturnsWarningStruct(testCase)
            converter = mcpserver.internal.output.converter.PlainTextWarningConverter();
            payload = struct('message', 'something went wrong', 'identifier', 'test:warn', 'wasDisabled', false);
            evt = struct('type', 'IssuedWarning', 'payload', payload);

            result = converter.convert(evt);

            testCase.verifyEqual(result.outputType, 'warning');
            testCase.verifyEqual(result.text, 'something went wrong');
            testCase.verifyEqual(result.identifier, 'test:warn');
        end

        function testPlainTextWarningConverter_Convert_StringFields_ReturnsChar(testCase)
            converter = mcpserver.internal.output.converter.PlainTextWarningConverter();
            payload = struct('message', "a string message", 'identifier', "my:id", 'wasDisabled', false);
            evt = struct('type', 'IssuedWarning', 'payload', payload);

            result = converter.convert(evt);

            testCase.verifyClass(result.text, 'char');
            testCase.verifyClass(result.identifier, 'char');
            testCase.verifyEqual(result.text, 'a string message');
            testCase.verifyEqual(result.identifier, 'my:id');
        end

        function testPlainTextWarningConverter_Convert_EmptyMessage_ReturnsEmptyChar(testCase)
            converter = mcpserver.internal.output.converter.PlainTextWarningConverter();
            payload = struct('message', '', 'identifier', 'test:empty', 'wasDisabled', false);
            evt = struct('type', 'IssuedWarning', 'payload', payload);

            result = converter.convert(evt);

            testCase.verifyEqual(result.text, '');
            testCase.verifyEqual(result.identifier, 'test:empty');
        end
    end

end
