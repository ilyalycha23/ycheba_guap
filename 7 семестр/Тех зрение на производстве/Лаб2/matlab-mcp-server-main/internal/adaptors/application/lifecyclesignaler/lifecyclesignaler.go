// Copyright 2025 The MathWorks, Inc.

package lifecyclesignaler

import (
	"context"
	"sync"
	"time"

	"golang.org/x/sync/errgroup"
)

// 2 minute might seem long, but we need to shutdown a MATLAB process gracefully
const defaultShutdownTimeout time.Duration = 2 * time.Minute

type LifecycleSignaler struct {
	shutdownC       chan struct{}
	shutdownWG      *errgroup.Group
	shutdownOnce    *sync.Once
	shutdownTimeout time.Duration
}

func New() *LifecycleSignaler {
	lifecycleSignaler := &LifecycleSignaler{
		shutdownC:       make(chan struct{}),
		shutdownWG:      new(errgroup.Group),
		shutdownOnce:    new(sync.Once),
		shutdownTimeout: defaultShutdownTimeout,
	}
	return lifecycleSignaler
}

func (r *LifecycleSignaler) RequestShutdown() {
	r.shutdownOnce.Do(func() {
		close(r.shutdownC)
	})
}

func (r *LifecycleSignaler) AddShutdownFunction(fcn func() error) {
	r.shutdownWG.Go(func() error {
		<-r.shutdownC
		return fcn()
	})
}

func (r *LifecycleSignaler) WaitForShutdownToComplete() error {
	<-r.shutdownC

	ctx, cancel := context.WithTimeout(context.Background(), r.shutdownTimeout)
	defer cancel()

	errC := make(chan error)
	go func() {
		errC <- r.shutdownWG.Wait()
	}()

	select {
	case err := <-errC:
		return err
	case <-ctx.Done():
		if err := ctx.Err(); err != nil && err != context.Canceled {
			return err
		}
		return nil
	}
}
