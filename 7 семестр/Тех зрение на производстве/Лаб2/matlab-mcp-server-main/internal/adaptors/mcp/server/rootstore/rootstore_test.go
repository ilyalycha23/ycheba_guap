// Copyright 2026 The MathWorks, Inc.

package rootstore_test

import (
	"testing"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/mcp/server/rootstore"
	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/modelcontextprotocol/go-sdk/mcp"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestRootStore_New_HappyPath(t *testing.T) {
	// Arrange
	// (no setup needed)

	// Act
	store := rootstore.New()

	// Assert
	assert.NotNil(t, store, "RootStore instance should not be nil")
}

func TestRootStore_GetRoots_ReturnsEmptySliceWhenNoRootsSet(t *testing.T) {
	// Arrange
	store := rootstore.New()

	// Act
	roots := store.GetRoots()

	// Assert
	require.NotNil(t, roots, "GetRoots should return a non-nil slice")
	assert.Empty(t, roots, "GetRoots should return an empty slice when no roots have been set")
}

func TestRootStore_UpdateRoots_ThenGetRootsReturnsCachedRoots(t *testing.T) {
	// Arrange
	store := rootstore.New()

	rootURI1 := "root-uri-1"
	rootURI2 := "root-uri-2"
	inputRoots := []*mcp.Root{
		{URI: rootURI1},
		{URI: rootURI2},
	}

	expectedRoots := []entities.MCPRoot{
		entities.NewMCPRoot(rootURI1, ""),
		entities.NewMCPRoot(rootURI2, ""),
	}

	// Act
	store.UpdateRoots(inputRoots)
	roots := store.GetRoots()

	// Assert
	require.Len(t, roots, 2, "GetRoots should return 2 roots")
	assert.Equal(t, expectedRoots, roots, "GetRoots should return the roots that were set via Update")
}

func TestRootStore_UpdateRoots_ReplacesExistingRoots(t *testing.T) {
	// Arrange
	store := rootstore.New()

	firstRootURI := "first-root-uri"
	firstRoots := []*mcp.Root{
		{URI: firstRootURI},
	}

	secondRootURI := "second-root-uri"
	secondRoots := []*mcp.Root{
		{URI: secondRootURI},
	}

	expectedRoots := []entities.MCPRoot{
		entities.NewMCPRoot(secondRootURI, ""),
	}

	// Act
	store.UpdateRoots(firstRoots)
	store.UpdateRoots(secondRoots)
	roots := store.GetRoots()

	// Assert
	require.Len(t, roots, 1, "GetRoots should return 1 root after second Update")
	assert.Equal(t, expectedRoots, roots, "GetRoots should return the roots from the second Update call")
}

func TestRootStore_GetRoots_ReturnsDefensiveCopy(t *testing.T) {
	// Arrange
	store := rootstore.New()

	rootURI := "original-root-uri"
	originalRoots := []*mcp.Root{
		{URI: rootURI},
	}
	store.UpdateRoots(originalRoots)

	// Act
	returnedRoots := store.GetRoots()
	returnedRoots[0] = entities.NewMCPRoot("modified-root-uri", "")

	roots := store.GetRoots()

	// Assert
	require.Len(t, roots, 1, "Internal state should still have 1 root")
	assert.Equal(t, rootURI, roots[0].URI(), "Internal state should not be affected by modifying the returned slice")
}

func TestRootStore_UpdateRoots_StoresDefensiveCopy(t *testing.T) {
	// Arrange
	store := rootstore.New()

	rootURI := "original-root-uri"
	inputRoots := []*mcp.Root{
		{URI: rootURI},
	}
	store.UpdateRoots(inputRoots)

	// Act
	inputRoots[0] = &mcp.Root{URI: "modified-root-uri"}

	roots := store.GetRoots()

	// Assert
	require.Len(t, roots, 1, "Internal state should still have 1 root")
	assert.Equal(t, rootURI, roots[0].URI(), "Internal state should not be affected by modifying the input slice")
}

func TestRootStore_UpdateRoots_WithNilSliceThenGetRootsReturnsEmptySlice(t *testing.T) {
	// Arrange
	store := rootstore.New()

	// Act
	store.UpdateRoots(nil)
	roots := store.GetRoots()

	// Assert
	assert.Empty(t, roots, "GetRoots should return an empty slice after Update(nil)")
}

func TestRootStore_UpdateRoots_WithEmptySliceThenGetRootsReturnsEmptySlice(t *testing.T) {
	// Arrange
	store := rootstore.New()

	// Act
	store.UpdateRoots([]*mcp.Root{})
	roots := store.GetRoots()

	// Assert
	assert.Empty(t, roots, "GetRoots should return an empty slice after Update with empty slice")
}

func TestRootStore_UpdateRoots_SkipsNilEntries(t *testing.T) {
	// Arrange
	store := rootstore.New()

	rootURI := "valid-root-uri"
	inputRoots := []*mcp.Root{
		nil,
		{URI: rootURI},
		nil,
	}

	expectedRoots := []entities.MCPRoot{
		entities.NewMCPRoot(rootURI, ""),
	}

	// Act
	store.UpdateRoots(inputRoots)
	roots := store.GetRoots()

	// Assert
	require.Len(t, roots, 1, "GetRoots should return only non-nil roots")
	assert.Equal(t, expectedRoots, roots, "GetRoots should skip nil entries")
}
