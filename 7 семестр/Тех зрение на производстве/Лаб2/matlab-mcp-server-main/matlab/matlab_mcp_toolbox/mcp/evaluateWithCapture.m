function results = evaluateWithCapture(code, options)
    %evaluateWithCapture Evaluate MATLAB code with output capture and figure control

    % Copyright 2026 The MathWorks, Inc.

    arguments
        code(1, 1) string
        options.ShowFigureWindows(1, 1) logical
        options.DisplayCapturedEvents(1, 1) logical
        options.DisplayDuringExecution(1, 1) logical
    end

    args = namedargs2cell(options);
    results = mcpserver.internal.evaluateWithCapture(code, args{:});
end
