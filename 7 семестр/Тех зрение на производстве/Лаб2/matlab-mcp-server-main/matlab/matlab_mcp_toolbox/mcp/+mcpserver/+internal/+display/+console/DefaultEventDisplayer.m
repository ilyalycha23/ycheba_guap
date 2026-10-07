classdef DefaultEventDisplayer < mcpserver.internal.display.console.EventDisplayer
    %DefaultEventDisplayer Renders captured events to the MATLAB console

    % Copyright 2026 The MathWorks, Inc.

    methods
        function displayEvents(~, capturedEvents)
            render(capturedEvents);
        end
    end

end

function render(capturedEvents)
    import mcpserver.internal.capture.EventType

    for i = 1:numel(capturedEvents)
        evt = capturedEvents(i);
        switch EventType.fromEvent(evt)
            case EventType.Stdout
                renderStdout(evt);
            case EventType.Stderr
                renderStderr(evt);
            case EventType.VariableDisplay
                renderVariable(evt);
            case EventType.IssuedWarning
                renderWarning(evt);
            otherwise
                % Figure events are rendered by the MATLAB graphics
                % pipeline; Unknown events are silently skipped.
        end
    end
end

function renderStdout(evt)
    fprintf('%s', evt.payload);
end

function renderStderr(evt)
    fprintf(2, '%s', evt.payload);
end

function renderVariable(evt)
    eval([evt.payload.name ' = evt.payload.value']);
end

function renderWarning(evt)
    previousBacktrace = warning('query', 'backtrace');
    warning('off', 'backtrace');
    cleanup = onCleanup(@() warning(previousBacktrace.state, 'backtrace'));
    if ~isempty(evt.payload.identifier)
        warning(evt.payload.identifier, '%s', evt.payload.message);
    else
        warning('%s', evt.payload.message);
    end
end
