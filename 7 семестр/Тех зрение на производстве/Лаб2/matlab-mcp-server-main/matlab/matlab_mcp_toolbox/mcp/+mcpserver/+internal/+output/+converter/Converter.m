classdef (Abstract) Converter
    %Converter Abstract interface for event output converters

    % Copyright 2026 The MathWorks, Inc.

    methods (Abstract)
        out = convert(obj, evt)
    end

end
