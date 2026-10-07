// Copyright 2026 The MathWorks, Inc.

package rootstore

import (
	"slices"
	"sync"

	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type RootStore struct {
	mu    sync.RWMutex
	roots []entities.MCPRoot
}

func New() *RootStore {
	return &RootStore{}
}

func (rs *RootStore) UpdateRoots(roots []*mcp.Root) {
	rs.mu.Lock()
	defer rs.mu.Unlock()

	converted := make([]entities.MCPRoot, 0, len(roots))
	for _, r := range roots {
		if r == nil {
			continue
		}
		converted = append(converted, entities.NewMCPRoot(r.URI, r.Name))
	}
	rs.roots = converted
}

// GetRoots returns a copy of the cached list of roots.
// Returns an empty slice if no roots have been set.
func (rs *RootStore) GetRoots() []entities.MCPRoot {
	rs.mu.RLock()
	defer rs.mu.RUnlock()
	if rs.roots == nil {
		return []entities.MCPRoot{}
	}
	return slices.Clone(rs.roots)
}
