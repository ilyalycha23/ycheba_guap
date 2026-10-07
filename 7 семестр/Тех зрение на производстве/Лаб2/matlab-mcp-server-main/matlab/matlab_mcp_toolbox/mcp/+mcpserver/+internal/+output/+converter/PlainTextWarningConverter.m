classdef PlainTextWarningConverter < mcpserver.internal.output.converter.Converter
    %PlainTextWarningConverter Converts warning events to plain text

    % Copyright 2026 The MathWorks, Inc.

    methods
        function out = convert(~, evt)
            out = struct( ...
                'outputType', 'warning', ...
                'identifier', char(string(evt.payload.identifier)), ...
                'text', char(string(evt.payload.message)) ...
            );
        end
    end

end
