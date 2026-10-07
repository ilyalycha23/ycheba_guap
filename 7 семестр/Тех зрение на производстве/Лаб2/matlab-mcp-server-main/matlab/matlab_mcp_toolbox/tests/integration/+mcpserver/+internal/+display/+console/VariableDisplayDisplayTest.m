classdef VariableDisplayDisplayTest < mcpserver.internal.display.console.DisplayTestHelper
    %VariableDisplayDisplayTest Integration tests for variable display console rendering

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testScalar_DisplaysNameAndValue(testCase)
            consoleOutput = testCase.captureAndDisplay("x = 42");

            testCase.verifySubstring(consoleOutput, "x =");
            testCase.verifySubstring(consoleOutput, "42");
        end

        function testString_DisplaysNameAndValue(testCase)
            consoleOutput = testCase.captureAndDisplay("s = ""hello""");

            testCase.verifySubstring(consoleOutput, "s =");
            testCase.verifySubstring(consoleOutput, "hello");
        end

        function testChar_DisplaysNameAndValue(testCase)
            consoleOutput = testCase.captureAndDisplay("c = 'abc'");

            testCase.verifySubstring(consoleOutput, "c =");
            testCase.verifySubstring(consoleOutput, "abc");
        end

        function testMatrix_DisplaysName(testCase)
            consoleOutput = testCase.captureAndDisplay("M = magic(3)");

            testCase.verifySubstring(consoleOutput, "M =");
        end

        function testVector_DisplaysNameAndValues(testCase)
            consoleOutput = testCase.captureAndDisplay("v = [1 2 3]");

            testCase.verifySubstring(consoleOutput, "v =");
            testCase.verifySubstring(consoleOutput, "1");
            testCase.verifySubstring(consoleOutput, "2");
            testCase.verifySubstring(consoleOutput, "3");
        end

        function testLogical_DisplaysNameAndValue(testCase)
            consoleOutput = testCase.captureAndDisplay("flag = true");

            testCase.verifySubstring(consoleOutput, "flag =");
        end

        function testStruct_DisplaysName(testCase)
            consoleOutput = testCase.captureAndDisplay("S = struct('a', 1, 'b', 'text')");

            testCase.verifySubstring(consoleOutput, "S =");
        end

        function testCellArray_DisplaysName(testCase)
            consoleOutput = testCase.captureAndDisplay("C = {1, 'two', [3 4]}");

            testCase.verifySubstring(consoleOutput, "C =");
        end

        function testTable_DisplaysName(testCase)
            consoleOutput = testCase.captureAndDisplay( ...
                "T = table([1;2;3], {'a';'b';'c'}, VariableNames={'Num','Char'})");

            testCase.verifySubstring(consoleOutput, "T =");
        end

        function testDatetime_DisplaysName(testCase)
            consoleOutput = testCase.captureAndDisplay("dt = datetime('now')");

            testCase.verifySubstring(consoleOutput, "dt =");
        end

        function testDuration_DisplaysName(testCase)
            consoleOutput = testCase.captureAndDisplay("d = hours(2) + minutes(30)");

            testCase.verifySubstring(consoleOutput, "d =");
        end

        function testCategorical_DisplaysName(testCase)
            consoleOutput = testCase.captureAndDisplay( ...
                "cat = categorical({'red','green','blue'})");

            testCase.verifySubstring(consoleOutput, "cat =");
        end

        function testComplex_DisplaysName(testCase)
            consoleOutput = testCase.captureAndDisplay("z = 3 + 4i");

            testCase.verifySubstring(consoleOutput, "z =");
        end

        function testSparse_DisplaysName(testCase)
            consoleOutput = testCase.captureAndDisplay("sp = sparse(eye(3))");

            testCase.verifySubstring(consoleOutput, "sp =");
        end

        function testAns_DisplaysAns(testCase)
            consoleOutput = testCase.captureAndDisplay("1 + 1");

            testCase.verifySubstring(consoleOutput, "ans =");
            testCase.verifySubstring(consoleOutput, "2");
        end

        function testSuppressedAssignment_NoOutput(testCase)
            consoleOutput = testCase.captureAndDisplay("x = 42;");

            testCase.verifyThat(consoleOutput, ...
                ~matlab.unittest.constraints.ContainsSubstring("x ="), ...
                "Suppressed assignment should not display variable");
        end

        function testLargeMatrix_DisplaysName(testCase)
            consoleOutput = testCase.captureAndDisplay("big = ones(100, 100)");

            testCase.verifySubstring(consoleOutput, "big =");
        end
    end

end
