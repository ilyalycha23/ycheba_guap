// Copyright 2026 The MathWorks, Inc.

package rootpathresolver

import (
	"fmt"
	"net/url"
	"path/filepath"
	"strings"
	"unicode"

	"github.com/matlab/matlab-mcp-server/internal/entities"
)

type OSLayer interface {
	GOOS() string
	IsAbs(path string) bool
}

type RootPathResolver struct {
	osLayer OSLayer
}

func New(osLayer OSLayer) *RootPathResolver {
	return &RootPathResolver{osLayer: osLayer}
}

// Resolve converts a Root's file:// URI to a local filesystem path.
// Returns an error for non-file schemes, UNC paths, or non-absolute paths.
func (r *RootPathResolver) Resolve(root entities.MCPRoot) (string, error) {
	parsed, err := url.Parse(root.URI())
	if err != nil {
		return "", err
	}

	if parsed.Scheme != "file" {
		return "", fmt.Errorf("unsupported URI scheme %q: %s", parsed.Scheme, root.URI())
	}

	if parsed.Host != "" {
		return "", fmt.Errorf("UNC paths are not supported: %s", root.URI())
	}

	path := parsed.Path

	if r.osLayer.GOOS() == "windows" {
		// Detect UNC-style paths that slip through with an empty host.
		// e.g., file:////server/share parses as Host="" and Path="//server/share".
		// This check is Windows-only because double slashes are valid on Unix
		// (they are treated the same as a single slash), whereas UNC paths are
		// a Windows-only concept.
		if strings.HasPrefix(path, "//") {
			return "", fmt.Errorf("UNC paths are not supported: %s", root.URI())
		}

		// url.Parse("file:///C:/Users") produces Path="/C:/Users".
		// The leading slash must be stripped to form a valid Windows path (C:\Users).
		// Note: filepath.Clean does NOT handle this — on Windows it treats \C:\Users
		// as a rooted path and preserves the leading backslash.
		path = stripLeadingSlashBeforeDriveLetter(path)
	}

	if !r.osLayer.IsAbs(path) {
		return "", fmt.Errorf("root path is not absolute: %s", root.URI())
	}

	return filepath.FromSlash(path), nil
}

// stripLeadingSlashBeforeDriveLetter handles the url.Parse artifact where
// file:///C:/path produces Path="/C:/path". Returns "C:/path" if a drive
// letter pattern is found, otherwise returns the path unchanged.
func stripLeadingSlashBeforeDriveLetter(path string) string {
	if len(path) >= 3 && path[0] == '/' && unicode.IsLetter(rune(path[1])) && path[2] == ':' {
		return strings.TrimPrefix(path, "/")
	}
	return path
}
