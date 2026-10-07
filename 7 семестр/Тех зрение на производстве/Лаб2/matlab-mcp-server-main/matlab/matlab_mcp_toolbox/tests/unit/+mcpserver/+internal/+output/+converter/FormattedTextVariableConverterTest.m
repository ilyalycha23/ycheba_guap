classdef FormattedTextVariableConverterTest < matlab.unittest.TestCase
    %FormattedTextVariableConverterTest Unit tests for FormattedTextVariableConverter

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testFormattedTextVariableConverter_Convert_NumericScalar_ReturnsVariableStruct(testCase)
            converter = mcpserver.internal.output.converter.FormattedTextVariableConverter();
            payload = struct('name', 'x', 'value', 42);
            evt = struct('type', 'VariableDisplay', 'payload', payload);

            result = converter.convert(evt);

            testCase.verifyEqual(result.outputType, 'variable');
            testCase.verifyEqual(result.name, 'x');
            testCase.verifySubstring(result.text, '42');
        end

        function testFormattedTextVariableConverter_Convert_StringName_ReturnsChar(testCase)
            converter = mcpserver.internal.output.converter.FormattedTextVariableConverter();
            payload = struct('name', "myVar", 'value', 1);
            evt = struct('type', 'VariableDisplay', 'payload', payload);

            result = converter.convert(evt);

            testCase.verifyClass(result.name, 'char');
            testCase.verifyEqual(result.name, 'myVar');
        end

        function testFormattedTextVariableConverter_Convert_Matrix_ReturnsFormattedText(testCase)
            converter = mcpserver.internal.output.converter.FormattedTextVariableConverter();
            payload = struct('name', 'M', 'value', [1 2; 3 4]);
            evt = struct('type', 'VariableDisplay', 'payload', payload);

            result = converter.convert(evt);

            testCase.verifyEqual(result.outputType, 'variable');
            testCase.verifyEqual(result.name, 'M');
            testCase.verifyClass(result.text, 'char');
            testCase.verifySubstring(result.text, '1');
            testCase.verifySubstring(result.text, '4');
        end

        function testFormattedTextVariableConverter_Convert_CharArray_ReturnsFormattedText(testCase)
            converter = mcpserver.internal.output.converter.FormattedTextVariableConverter();
            payload = struct('name', 'str', 'value', 'hello');
            evt = struct('type', 'VariableDisplay', 'payload', payload);

            result = converter.convert(evt);

            testCase.verifyEqual(result.outputType, 'variable');
            testCase.verifyEqual(result.name, 'str');
            testCase.verifySubstring(result.text, 'hello');
        end
    end

end
