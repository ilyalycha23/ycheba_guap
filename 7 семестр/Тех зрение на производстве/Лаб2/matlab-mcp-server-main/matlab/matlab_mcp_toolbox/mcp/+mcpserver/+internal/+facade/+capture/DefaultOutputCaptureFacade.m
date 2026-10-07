classdef DefaultOutputCaptureFacade < mcpserver.internal.facade.capture.OutputCaptureFacade
    %DefaultOutputCaptureFacade Implementation using MATLAB internal builtins and features

    % Copyright 2026 The MathWorks, Inc.

    methods
        function value = getAllowOutputCapture(~)
            value = feature('AllowOutputCapture');
        end

        function setAllowOutputCapture(~, value)
            feature('AllowOutputCapture', value);
        end

        function value = getSuppressCommandLineOutput(~)
            value = feature('SuppressCommandLineOutput');
        end

        function setSuppressCommandLineOutput(~, value)
            feature('SuppressCommandLineOutput', value);
        end

        function value = getHotlinks(~)
            value = feature('hotlinks');
        end

        function setHotlinks(~, value)
            feature('hotlinks', value);
        end

        function pushTextOutputListeners(~)
            builtin('_setTextOutputListeners', 'push');
        end

        function popTextOutputListeners(~)
            builtin('_setTextOutputListeners', 'pop');
        end

        function resetStructuredFigures(~)
            builtin('_StructuredFiguresResetAll');
        end
    end

end
