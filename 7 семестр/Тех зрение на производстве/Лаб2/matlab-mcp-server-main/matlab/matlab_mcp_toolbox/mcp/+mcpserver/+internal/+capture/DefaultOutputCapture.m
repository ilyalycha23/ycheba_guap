classdef DefaultOutputCapture < mcpserver.internal.capture.OutputCapture
    %DefaultOutputCapture Implementation using MATLAB output capture builtins

    % Copyright 2026 The MathWorks, Inc.

    properties (GetAccess = private, SetAccess = immutable)
        Facade(1, 1) mcpserver.internal.facade.capture.OutputCaptureFacade = mcpserver.internal.facade.capture.DefaultOutputCaptureFacade()
    end

    properties (Access = private)
        IsEnabled(1, 1) logical = false
        OriginalAllowCapture
        OriginalSuppressOutput
        OriginalHotlinks
    end

    methods
        function obj = DefaultOutputCapture(options)
            arguments
                options.?mcpserver.internal.capture.DefaultOutputCapture
            end

            for prop = string(fieldnames(options).')
                obj.(prop) = options.(prop);
            end
        end

        function enable(obj)
            if obj.IsEnabled
                return;
            end
            obj.OriginalAllowCapture = obj.Facade.getAllowOutputCapture();
            obj.OriginalSuppressOutput = obj.Facade.getSuppressCommandLineOutput();
            obj.OriginalHotlinks = obj.Facade.getHotlinks();
            obj.Facade.pushTextOutputListeners();
            obj.IsEnabled = true;
            obj.Facade.resetStructuredFigures();
            obj.Facade.setAllowOutputCapture(true);
            obj.Facade.setSuppressCommandLineOutput(true);
            obj.Facade.setHotlinks(false);
        end

        function disable(obj)
            if ~obj.IsEnabled
                return;
            end
            obj.Facade.popTextOutputListeners();
            obj.Facade.setAllowOutputCapture(obj.OriginalAllowCapture);
            obj.Facade.setSuppressCommandLineOutput(obj.OriginalSuppressOutput);
            obj.Facade.setHotlinks(obj.OriginalHotlinks);
            obj.IsEnabled = false;
        end

        function runUncaptured(obj, fcn)
            if ~obj.IsEnabled
                fcn();
                return;
            end
            obj.disable();
            cleanup = onCleanup(@() obj.enable());
            fcn();
        end

        function delete(obj)
            obj.disable();
        end
    end

end
