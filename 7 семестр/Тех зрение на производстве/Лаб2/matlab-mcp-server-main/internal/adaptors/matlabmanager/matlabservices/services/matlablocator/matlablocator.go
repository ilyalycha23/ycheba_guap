// Copyright 2025-2026 The MathWorks, Inc.

package matlablocator

import (
	"github.com/matlab/matlab-mcp-server/internal/adaptors/matlabmanager/matlabservices/datatypes"
	"github.com/matlab/matlab-mcp-server/internal/entities"
)

type MATLABRootGetter interface {
	GetAll(logger entities.Logger) []string
}

type MATLABVersionGetter interface {
	Get(matlabRootLocation string) (datatypes.MatlabVersionInfo, error)
}

type MATLABLocator struct {
	matlabRootGetter    MATLABRootGetter
	matlabVersionGetter MATLABVersionGetter
}

func New(
	matlabRootGetter MATLABRootGetter,
	matlabVersionGetter MATLABVersionGetter,
) *MATLABLocator {
	return &MATLABLocator{
		matlabRootGetter:    matlabRootGetter,
		matlabVersionGetter: matlabVersionGetter,
	}
}

func (s *MATLABLocator) ListDiscoveredMatlabInfo(logger entities.Logger) datatypes.ListMatlabInfo {
	discoveredMatlabLocations := s.matlabRootGetter.GetAll(logger)

	infos := make([]datatypes.MatlabInfo, 0)
	for _, matlabLocation := range discoveredMatlabLocations {
		info, err := s.getVerifiedEnvironmentFromLocation(matlabLocation)
		if err != nil {
			logger.With("matlab_root", matlabLocation).WithError(err).Warn("Possible MATLAB location candidate was invalid.")
			continue
		}
		infos = append(infos, info)
	}

	if len(infos) == 0 {
		return datatypes.ListMatlabInfo{}
	}

	return datatypes.ListMatlabInfo{
		MatlabInfo: infos,
	}
}

func (s *MATLABLocator) getVerifiedEnvironmentFromLocation(location string) (datatypes.MatlabInfo, error) {
	version, err := s.matlabVersionGetter.Get(location)
	if err != nil {
		return datatypes.MatlabInfo{}, err
	}

	return datatypes.MatlabInfo{
		Version:  version,
		Location: location,
	}, nil
}
