classdef EventType
    %EventType Classification of structured output events

    % Copyright 2026 The MathWorks, Inc.

    enumeration
        Stdout
        Stderr
        VariableDisplay
        IssuedWarning
        Figure
        Unknown
    end

    methods (Static)
        function t = fromEvent(evt)
            import mcpserver.internal.capture.EventType

            if ~isfield(evt, 'type')
                t = EventType.Unknown;
                return;
            end

            if ~isfield(evt, 'payload')
                t = EventType.Unknown;
                return;
            end

            switch evt.type
                case 'stdout'
                    t = EventType.Stdout;
                case 'stderr'
                    t = EventType.Stderr;
                case 'VariableDisplay'
                    if hasProperty(evt.payload, 'value')
                        t = EventType.VariableDisplay;
                    else
                        t = EventType.Unknown;
                    end
                case 'IssuedWarning'
                    if hasProperty(evt.payload, 'wasDisabled') && ~evt.payload.wasDisabled
                        t = EventType.IssuedWarning;
                    else
                        t = EventType.Unknown;
                    end
                case 'figure'
                    if isscalar(evt.payload) && ishghandle(evt.payload)
                        t = EventType.Figure;
                    else
                        t = EventType.Unknown;
                    end
                otherwise
                    t = EventType.Unknown;
            end
        end
    end

end

function tf = hasProperty(payload, name)
    if isstruct(payload)
        tf = isfield(payload, name);
    elseif isobject(payload)
        tf = isprop(payload, name);
    else
        tf = false;
    end
end
