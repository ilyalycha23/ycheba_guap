// Copyright 2026 The MathWorks, Inc.

package mcpbstagebuilder

import (
	"bytes"
	"embed"
	"encoding/json"
	"errors"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strings"

	"github.com/matlab/matlab-mcp-server/internal/adaptors/mcpb/tools"
	"github.com/matlab/matlab-mcp-server/internal/adaptors/mcpb/userconfig"
)

//go:embed assets
var assets embed.FS

const (
	mcpbStagingDirEnvVar      = "MCPB_STAGING_DIR"
	folderPermissions         = 0o755
	filePermissions           = 0o644
	executableFilePermissions = 0o755
)

// Build stages all MCPB bundle artifacts into the staging directory
// specified by the MCPB_STAGING_DIR environment variable.
// It reads templates from the embedded assets and injects the resolved version.
func Build(version string) error {
	mcpbStaging, ok := os.LookupEnv(mcpbStagingDirEnvVar)
	if !ok {
		return errors.New(mcpbStagingDirEnvVar + " is unset")
	}

	if err := validateStagingDir(mcpbStaging); err != nil {
		return err
	}

	if _, err := os.Stat(mcpbStaging); err == nil {
		return fmt.Errorf("staging directory %q already exists; remove it first", mcpbStaging)
	} else if !errors.Is(err, os.ErrNotExist) {
		return fmt.Errorf("failed to stat staging directory %q: %w", mcpbStaging, err)
	}

	if err := os.MkdirAll(filepath.Join(mcpbStaging, "bundle", "bin"), folderPermissions); err != nil {
		return err
	}

	if err := stagePackageJSON(mcpbStaging, assets); err != nil {
		return err
	}

	if err := stageManifest(mcpbStaging, assets, version); err != nil {
		return err
	}

	if err := stageStaticAssets(mcpbStaging, assets); err != nil {
		return err
	}

	return nil
}

func validateStagingDir(path string) error {
	if path == "" {
		return errors.New("staging directory path is empty")
	}
	cleaned := filepath.Clean(path)
	if cleaned == "/" {
		return fmt.Errorf("refusing to use filesystem root %q as staging directory", path)
	}
	if vol := filepath.VolumeName(cleaned); vol != "" && cleaned == vol+string(filepath.Separator) {
		return fmt.Errorf("refusing to use filesystem root %q as staging directory", path)
	}
	return nil
}

func stagePackageJSON(mcpbStaging string, assets fs.FS) error {
	relativePath := "package.json"

	content, err := fs.ReadFile(assets, filepath.ToSlash(filepath.Join("assets", relativePath)))
	if err != nil {
		return fmt.Errorf("failed to read template: %w", err)
	}

	if err := os.WriteFile(filepath.Join(mcpbStaging, relativePath), content, filePermissions); err != nil {
		return fmt.Errorf("failed to write package.json: %w", err)
	}

	return nil
}

func stageManifest(mcpbStaging string, assets fs.FS, version string) error {
	relativePath := filepath.Join("bundle", "manifest.json")

	templateContent, err := fs.ReadFile(assets, filepath.ToSlash(filepath.Join("assets", relativePath)))
	if err != nil {
		return fmt.Errorf("failed to read template: %w", err)
	}

	var manifest map[string]any
	if err := json.Unmarshal(templateContent, &manifest); err != nil {
		return fmt.Errorf("failed to parse template: %w", err)
	}

	if version == "" {
		return fmt.Errorf("version is empty")
	}
	manifest["version"] = version

	toolDefs := tools.Definitions()
	if len(toolDefs) == 0 {
		return fmt.Errorf("no tools found")
	}

	toolsJSON := make([]any, len(toolDefs))
	for i, t := range toolDefs {
		toolsJSON[i] = map[string]string{
			"name":        t.Name,
			"description": t.Description,
		}
	}
	manifest["tools"] = toolsJSON

	userConfig, err := userconfig.GetUserConfig()
	if err != nil {
		return err
	}
	if len(userConfig) == 0 {
		return fmt.Errorf("no user_config entries found")
	}
	manifest["user_config"] = userConfig

	var buf bytes.Buffer
	enc := json.NewEncoder(&buf)
	enc.SetEscapeHTML(false)
	enc.SetIndent("", "  ")
	if err := enc.Encode(manifest); err != nil {
		return fmt.Errorf("failed to marshal manifest: %w", err)
	}

	if err := os.WriteFile(filepath.Join(mcpbStaging, relativePath), buf.Bytes(), filePermissions); err != nil {
		return fmt.Errorf("failed to write manifest: %w", err)
	}

	fmt.Printf("Generated %s (version %s) with %d tools and %d user_config entries\n", filepath.Join(mcpbStaging, relativePath), version, len(toolDefs), len(userConfig))
	return nil
}

func toCRLF(data []byte) []byte {
	normalized := bytes.ReplaceAll(data, []byte("\r\n"), []byte("\n"))
	return bytes.ReplaceAll(normalized, []byte("\n"), []byte("\r\n"))
}

func stageStaticAssets(mcpbStaging string, assets fs.FS) error {
	relativePath := filepath.Join("bundle", "icon.png")

	icon, err := fs.ReadFile(assets, filepath.ToSlash(filepath.Join("assets", relativePath)))
	if err != nil {
		return err
	}
	err = os.WriteFile(filepath.Join(mcpbStaging, relativePath), icon, filePermissions)
	if err != nil {
		return err
	}

	binPath := filepath.ToSlash(filepath.Join("assets", "bundle", "bin"))
	if err = fs.WalkDir(assets, binPath, func(path string, d fs.DirEntry, walkErr error) error {
		if walkErr != nil {
			return walkErr
		}

		if d.IsDir() {
			if path != binPath {
				return fs.SkipDir
			}
			return nil
		}

		fileName := strings.TrimPrefix(path, binPath+"/")

		fileContent, err := fs.ReadFile(assets, path)
		if err != nil {
			return err
		}
		if strings.HasSuffix(fileName, ".cmd") {
			fileContent = toCRLF(fileContent)
		}
		err = os.WriteFile(filepath.Join(mcpbStaging, "bundle", "bin", fileName), fileContent, executableFilePermissions)
		if err != nil {
			return err
		}

		return nil
	}); err != nil {
		return err
	}

	return nil
}
