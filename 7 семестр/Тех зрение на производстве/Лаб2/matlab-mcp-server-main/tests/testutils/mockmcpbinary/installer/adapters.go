// Copyright 2026 The MathWorks, Inc.

package installer

import (
	"encoding/json"
	"fmt"
	"os/exec"
)

type GoListModuleRootFinder struct{}

func (GoListModuleRootFinder) FindModuleRoot() (string, error) {
	output, err := exec.Command("go", "list", "-m", "-json").Output()
	if err != nil {
		return "", fmt.Errorf("running 'go list -m -json': %w", err)
	}

	var mod struct{ Dir string }
	if err := json.Unmarshal(output, &mod); err != nil {
		return "", fmt.Errorf("parsing module info: %w", err)
	}

	return mod.Dir, nil
}

type GoBinaryBuilder struct{}

func (GoBinaryBuilder) Build(sourceDir, outputPath string) error {
	cmd := exec.Command("go", "build", "-o", outputPath, ".")
	cmd.Dir = sourceDir
	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("%s: %w", output, err)
	}
	return nil
}
