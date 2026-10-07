// Copyright 2025-2026 The MathWorks, Inc.

package matlabmanager

import (
	"context"

	"github.com/matlab/matlab-mcp-server/internal/entities"
)

func (m *MATLABManager) ListEnvironments(_ context.Context, sessionLogger entities.Logger) []entities.EnvironmentInfo {
	sessionLogger.Debug("Calling ListDiscoveredMatlabInfo on MATLAB Manager")

	matlabInfos := m.matlabServices.ListDiscoveredMatlabInfo(sessionLogger)

	sessionLogger.With("count", len(matlabInfos.MatlabInfo)).Debug("Converting datatypes to entities")

	info := make([]entities.EnvironmentInfo, 0, len(matlabInfos.MatlabInfo))
	for _, matlabInfo := range matlabInfos.MatlabInfo {
		info = append(info, entities.EnvironmentInfo{
			MATLABRoot: matlabInfo.Location,
			Version:    matlabInfo.Version.ReleaseFamily,
		})
	}

	return info
}
