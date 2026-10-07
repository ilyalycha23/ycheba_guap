classdef PlainTextConsoleConverter < mcpserver.internal.output.converter.Converter
    %PlainTextConsoleConverter Converts stdout/stderr events to plain text

    % Copyright 2026 The MathWorks, Inc.

    methods
        function out = convert(~, evt)
            out = struct( ...
                'outputType', 'consoleOutput', ...
                'text', char(string(evt.payload)) ...
            );
        end
    end

end
