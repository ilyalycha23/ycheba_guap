classdef DefaultFigureVisibilityController < mcpserver.internal.display.FigureVisibilityController
    %DefaultFigureVisibilityController Controls figure visibility for the MCP server.
    %   Provides methods to hide or show figures independently of the
    %   display mode. Call hide() to suppress figure windows and show() to
    %   restore normal behavior. Use restore() to return to the state
    %   captured before the first hide() or show() call.

    % Copyright 2026 The MathWorks, Inc.

    properties (GetAccess = private, SetAccess = immutable)
        DisplayFacade(1, 1) mcpserver.internal.facade.display.DisplayFacade = mcpserver.internal.facade.display.DefaultDisplayFacade()
    end

    properties (Constant, Access = private)
        DefaultFigureVisibleProperty = "DefaultFigureVisible"
        DefaultFigureCreateFcnProperty = "DefaultFigureCreateFcn"
    end

    properties (Access = private)
        SavedDefaultFigureVisible
        SavedDefaultFigureCreateFcn
        HasSavedState(1, 1) logical = false
        FigureListeners = {}
    end

    methods
        function obj = DefaultFigureVisibilityController(options)
            arguments
                options.?mcpserver.internal.display.DefaultFigureVisibilityController
            end

            for prop = string(fieldnames(options).')
                obj.(prop) = options.(prop);
            end
        end

        function hide(obj)
            %hide Suppress figure windows.
            %   Saves the current figure visibility state, then sets
            %   DefaultFigureVisible to 'off' and installs a CreateFcn
            %   callback that locks every new figure to invisible.
            if ~obj.HasSavedState
                obj.saveState();
            end
            obj.DisplayFacade.setRootProperty(obj.DefaultFigureVisibleProperty, "off");
            obj.DisplayFacade.setRootProperty(obj.DefaultFigureCreateFcnProperty, @lockIfControllerValid);

            function lockIfControllerValid(fig, evt)
                if isvalid(obj)
                    obj.lockFigureVisibility(fig, evt);
                end
            end
        end

        function show(obj)
            %show Allow figure windows to display normally.
            %   Saves the current figure visibility state, then sets
            %   DefaultFigureVisible to 'on' and clears the CreateFcn
            %   callback. Removes any listeners installed by hide().
            if ~obj.HasSavedState
                obj.saveState();
            end
            obj.clearListeners();
            obj.DisplayFacade.setRootProperty(obj.DefaultFigureVisibleProperty, "on");
            obj.DisplayFacade.setRootProperty(obj.DefaultFigureCreateFcnProperty, "");
        end

        function delete(obj)
            obj.restore();
        end

        function restore(obj)
            %restore Restore figure visibility to the initial state captured
            %   before the first hide() or show() call. Does nothing if no
            %   state was saved.
            if ~obj.HasSavedState
                return;
            end
            obj.clearListeners();
            obj.DisplayFacade.setRootProperty(obj.DefaultFigureVisibleProperty, obj.SavedDefaultFigureVisible);
            obj.DisplayFacade.setRootProperty(obj.DefaultFigureCreateFcnProperty, obj.SavedDefaultFigureCreateFcn);
            obj.HasSavedState = false;
        end
    end

    methods (Access = private)
        function saveState(obj)
            obj.SavedDefaultFigureVisible = obj.DisplayFacade.getRootProperty(obj.DefaultFigureVisibleProperty);
            obj.SavedDefaultFigureCreateFcn = obj.DisplayFacade.getRootProperty(obj.DefaultFigureCreateFcnProperty);
            obj.HasSavedState = true;
        end

        function clearListeners(obj)
            for i = 1:numel(obj.FigureListeners)
                delete(obj.FigureListeners{i});
            end
            obj.FigureListeners = {};
        end

        function lockFigureVisibility(obj, fig, ~)
            fig.Visible = "off";
            listener = obj.DisplayFacade.addPropertyListener( ...
                fig, "Visible", "PostSet", @(~, ~) obj.enforceInvisible(fig));
            obj.FigureListeners{end + 1} = listener;
        end

        function enforceInvisible(~, fig)
            if ~isvalid(fig)
                return;
            end
            if fig.Visible ~= "off"
                fig.Visible = "off";
            end
        end
    end

end
