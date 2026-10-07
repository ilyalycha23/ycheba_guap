classdef FormattedTextVariableConverter < mcpserver.internal.output.converter.Converter
    %FormattedTextVariableConverter Converts variable display events using formattedDisplayText

    % Copyright 2026 The MathWorks, Inc.

    methods
        function out = convert(~, evt)
            out = struct( ...
                'outputType', 'variable', ...
                'name', char(string(evt.payload.name)), ...
                'text', char(string(formattedDisplayText(evt.payload.value, SuppressMarkup=true))) ...
            );
        end
    end

end
