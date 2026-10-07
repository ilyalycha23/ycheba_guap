classdef OutputBuilder
    %OutputBuilder Classifies captured events and dispatches to converters

    % Copyright 2026 The MathWorks, Inc.

    properties (GetAccess = private, SetAccess = immutable)
        ConverterMap
    end

    methods
        function obj = OutputBuilder(options)
            arguments
                options.StdoutConverter(1, 1) mcpserver.internal.output.converter.Converter = mcpserver.internal.output.converter.PlainTextConsoleConverter()
                options.StderrConverter(1, 1) mcpserver.internal.output.converter.Converter = mcpserver.internal.output.converter.PlainTextConsoleConverter()
                options.VariableDisplayConverter(1, 1) mcpserver.internal.output.converter.Converter = mcpserver.internal.output.converter.FormattedTextVariableConverter()
                options.WarningConverter(1, 1) mcpserver.internal.output.converter.Converter = mcpserver.internal.output.converter.PlainTextWarningConverter()
                options.FigureConverter(1, 1) mcpserver.internal.output.converter.Converter = mcpserver.internal.output.converter.Base64PngFigureConverter()
            end

            import mcpserver.internal.capture.EventType

            obj.ConverterMap = containers.Map();
            obj.ConverterMap(char(string(EventType.Stdout))) = options.StdoutConverter;
            obj.ConverterMap(char(string(EventType.Stderr))) = options.StderrConverter;
            obj.ConverterMap(char(string(EventType.VariableDisplay))) = options.VariableDisplayConverter;
            obj.ConverterMap(char(string(EventType.IssuedWarning))) = options.WarningConverter;
            obj.ConverterMap(char(string(EventType.Figure))) = options.FigureConverter;
        end

        function results = build(obj, events)
            import mcpserver.internal.capture.EventType

            results = {};

            for i = 1:numel(events)
                evt = events(i);
                evtType = EventType.fromEvent(evt);
                key = char(string(evtType));

                if obj.ConverterMap.isKey(key)
                    results{end+1} = obj.ConverterMap(key).convert(evt); %#ok<AGROW> % Final size unknown: events without a registered converter are skipped.
                end
            end
        end
    end

end
