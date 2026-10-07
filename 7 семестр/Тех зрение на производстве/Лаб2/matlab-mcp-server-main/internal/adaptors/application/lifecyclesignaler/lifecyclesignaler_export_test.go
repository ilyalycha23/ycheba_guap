// Copyright 2025 The MathWorks, Inc.

package lifecyclesignaler

import (
	"time"
)

// Only allow test to modify the shutdown timeout for now.

func (r *LifecycleSignaler) ShutdownTimeout() time.Duration {
	return r.shutdownTimeout
}

func (r *LifecycleSignaler) SetShutdownTimeout(timeout time.Duration) {
	r.shutdownTimeout = timeout
}
