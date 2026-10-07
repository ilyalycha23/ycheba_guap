classdef VariableDisplayCaptureTest < mcpserver.internal.capture.CaptureTestHelper
    %VariableDisplayCaptureTest Functional tests for VariableDisplay event capture

    % Copyright 2026 The MathWorks, Inc.

    methods (Test)
        function testScalarDisplay_ProducesVariableDisplayEvent(testCase)
            evalin('base', "x = 42");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Unsuppressed scalar assignment should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "x");
            testCase.verifyTrue(isnumeric(events(1).payload.value), ...
                "Scalar value should be numeric");
            testCase.verifyEqual(events(1).payload.value, 42);
        end

        function testSuppressedAssignment_NoVariableDisplayEvent(testCase)
            evalin('base', "x = 42;");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyEmpty(events, ...
                "Semicolon-suppressed assignment should not produce VariableDisplay");
        end

        function testSuppressedMatrix_NoVariableDisplayEvent(testCase)
            evalin('base', "M = magic(3);");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyEmpty(events, ...
                "Semicolon-suppressed matrix assignment should not produce VariableDisplay");
        end

        function testSuppressedString_NoVariableDisplayEvent(testCase)
            evalin('base', "s = ""hello"";");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyEmpty(events, ...
                "Semicolon-suppressed string assignment should not produce VariableDisplay");
        end

        function testSuppressedTable_NoVariableDisplayEvent(testCase)
            evalin('base', "T = table([1;2], {'a';'b'});");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyEmpty(events, ...
                "Semicolon-suppressed table assignment should not produce VariableDisplay");
        end

        function testStringDisplay_ProducesVariableDisplayEvent(testCase)
            evalin('base', "s = ""hello""");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "String assignment should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "s");
            testCase.verifyTrue(isstring(events(1).payload.value), ...
                "Value should be a string");
        end

        function testCharDisplay_ProducesVariableDisplayEvent(testCase)
            evalin('base', "c = 'abc'");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Char assignment should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "c");
            testCase.verifyTrue(ischar(events(1).payload.value), ...
                "Value should be a char array");
        end

        function testVectorDisplay_ProducesVariableDisplayEvent(testCase)
            evalin('base', "v = [1 2 3 4 5]");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Vector assignment should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "v");
            testCase.verifyTrue(isnumeric(events(1).payload.value), ...
                "Value should be numeric");
            testCase.verifyEqual(numel(events(1).payload.value), 5);
        end

        function testMatrixDisplay_ProducesVariableDisplayEvent(testCase)
            evalin('base', "M = magic(3)");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Matrix assignment should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "M");
            testCase.verifyTrue(isnumeric(events(1).payload.value), ...
                "Value should be numeric");
            testCase.verifyEqual(size(events(1).payload.value), [3 3]);
        end

        function testCellArrayDisplay_ProducesVariableDisplayEvent(testCase)
            evalin('base', "C = {1, 'two', [3 4]}");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Cell array assignment should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "C");
            testCase.verifyTrue(iscell(events(1).payload.value), ...
                "Value should be a cell array");
        end

        function testStructDisplay_ProducesVariableDisplayEvent(testCase)
            evalin('base', "S = struct('a', 1, 'b', 'text')");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Struct assignment should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "S");
            testCase.verifyTrue(isstruct(events(1).payload.value), ...
                "Value should be a struct");
        end

        function testLogicalDisplay_ProducesVariableDisplayEvent(testCase)
            evalin('base', "flag = true");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Logical assignment should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "flag");
            testCase.verifyTrue(islogical(events(1).payload.value), ...
                "Value should be logical");
        end

        function testTableDisplay_ProducesVariableDisplayEvent(testCase)
            evalin('base', "T = table([1;2;3], {'a';'b';'c'}, VariableNames={'Num','Char'})");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Table assignment should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "T");
            testCase.verifyTrue(istable(events(1).payload.value), ...
                "Value should be a table");
            testCase.verifyEqual(height(events(1).payload.value), 3);
        end

        function testTimetableDisplay_ProducesVariableDisplayEvent(testCase)
            evalin('base', "TT = timetable(seconds([1;2;3]), [10;20;30])");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Timetable assignment should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "TT");
            testCase.verifyTrue(istimetable(events(1).payload.value), ...
                "Value should be a timetable");
        end

        function testDatetimeDisplay_ProducesVariableDisplayEvent(testCase)
            evalin('base', "dt = datetime('now')");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Datetime assignment should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "dt");
            testCase.verifyTrue(isdatetime(events(1).payload.value), ...
                "Value should be a datetime");
        end

        function testDurationDisplay_ProducesVariableDisplayEvent(testCase)
            evalin('base', "d = hours(2) + minutes(30)");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Duration assignment should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "d");
            testCase.verifyTrue(isduration(events(1).payload.value), ...
                "Value should be a duration");
        end

        function testCategoricalDisplay_ProducesVariableDisplayEvent(testCase)
            evalin('base', "cat = categorical({'red','green','blue'})");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Categorical assignment should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "cat");
            testCase.verifyTrue(iscategorical(events(1).payload.value), ...
                "Value should be categorical");
        end

        function testComplexDisplay_ProducesVariableDisplayEvent(testCase)
            evalin('base', "z = 3 + 4i");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Complex number assignment should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "z");
            testCase.verifyTrue(isnumeric(events(1).payload.value), ...
                "Value should be numeric");
            testCase.verifyTrue(~isreal(events(1).payload.value), ...
                "Value should be complex");
        end

        function testSparseDisplay_ProducesVariableDisplayEvent(testCase)
            evalin('base', "sp = sparse(eye(3))");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Sparse matrix assignment should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "sp");
            testCase.verifyTrue(issparse(events(1).payload.value), ...
                "Value should be sparse");
        end

        function testMissingDisplay_ProducesVariableDisplayEvent(testCase)
            evalin('base', "m = missing");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Missing value display should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "m");
            testCase.verifyTrue(ismissing(events(1).payload.value), ...
                "Value should be missing");
        end

        function testDictionaryDisplay_ProducesStdoutEvent(testCase)
            evalin('base', "d = dictionary('a', 1, 'b', 2)");
            drawnow;
            testCase.Capture.disable();

            allEvents = testCase.EventProvider.getEvents();
            stdoutEvents = testCase.filterByType(allEvents, 'stdout');
            varEvents = testCase.filterByType(allEvents, 'VariableDisplay');

            hasOutput = ~isempty(stdoutEvents) || ~isempty(varEvents);
            testCase.verifyTrue(hasOutput, ...
                "Dictionary display should produce either stdout or VariableDisplay events");
        end

        function testLargeMatrix_ProducesVariableDisplayEvent(testCase)
            evalin('base', "big = ones(100, 100)");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Large matrix display should produce VariableDisplay");
            testCase.verifyEqual(string(events(1).payload.name), "big");
            testCase.verifyTrue(isnumeric(events(1).payload.value), ...
                "Value should be numeric");
            testCase.verifyEqual(size(events(1).payload.value), [100 100]);
        end

        function testAns_ProducesVariableDisplayEvent(testCase)
            evalin('base', "1 + 1");
            drawnow;
            testCase.Capture.disable();

            events = testCase.filterByType(testCase.EventProvider.getEvents(), 'VariableDisplay');

            testCase.verifyNotEmpty(events, "Unassigned expression should produce VariableDisplay for ans");
            testCase.verifyEqual(string(events(1).payload.name), "ans");
            testCase.verifyEqual(events(1).payload.value, 2);
        end
    end

end
