// Copyright 2025-2026 The MathWorks, Inc.

// This package implements a watchdog to run alongside this MCP Server.
// As the MCP Server may start multiple external dependencies (e.g. MATLAB processes), in the event of forceful shutdown,
// this watchdog ensures proper termination and cleanup of the external dependencies.
package watchdog
