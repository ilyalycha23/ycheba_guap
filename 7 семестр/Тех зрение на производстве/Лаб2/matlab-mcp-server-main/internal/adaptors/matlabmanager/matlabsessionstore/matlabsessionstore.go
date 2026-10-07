// Copyright 2025-2026 The MathWorks, Inc.

package matlabsessionstore

import (
	"context"
	"fmt"
	"sync"

	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/messages"
	"golang.org/x/sync/errgroup"
)

type LoggerFactory interface {
	GetGlobalLogger() (entities.Logger, messages.Error)
}

type MATLABSessionClientWithCleanup interface {
	entities.MATLABSessionClient
	StopSession(ctx context.Context, sessionLogger entities.Logger) error
}

type LifecycleSignaler interface {
	AddShutdownFunction(shutdownFcn func() error)
}

type storedSession struct {
	client        MATLABSessionClientWithCleanup
	correlationID string
}

type Store struct {
	l        *sync.RWMutex
	next     entities.SessionID
	sessions map[entities.SessionID]storedSession
}

func New(
	loggerFactory LoggerFactory,
	lifecycleSignaler LifecycleSignaler,
) *Store {
	store := &Store{
		l:        new(sync.RWMutex),
		next:     1,
		sessions: map[entities.SessionID]storedSession{},
	}

	lifecycleSignaler.AddShutdownFunction(func() error {
		store.l.Lock()
		defer store.l.Unlock()

		logger, err := loggerFactory.GetGlobalLogger()
		if err != nil {
			return err
		}

		wg := new(errgroup.Group)

		for sessionID, session := range store.sessions {
			wg.Go(func() error {
				err := session.client.StopSession(context.Background(), logger)
				if err != nil {
					return fmt.Errorf("error stopping session %v: %w", sessionID, err)
				}
				return nil
			})
		}

		return wg.Wait()
	})

	return store
}

func (s *Store) Add(client MATLABSessionClientWithCleanup, correlationID string) entities.SessionID {
	s.l.Lock()
	defer s.l.Unlock()

	sessionID := s.next
	s.sessions[sessionID] = storedSession{client: client, correlationID: correlationID}
	s.next++
	return entities.SessionID(sessionID)
}

func (s *Store) Get(sessionID entities.SessionID) (MATLABSessionClientWithCleanup, error) {
	s.l.RLock()
	defer s.l.RUnlock()

	session, exists := s.sessions[sessionID]
	if !exists {
		return nil, fmt.Errorf("session not found: %v", sessionID)
	}

	return session.client, nil
}

func (s *Store) CorrelationID(sessionID entities.SessionID) string {
	s.l.RLock()
	defer s.l.RUnlock()

	session, exists := s.sessions[sessionID]
	if !exists {
		return ""
	}

	return session.correlationID
}

func (s *Store) Remove(sessionID entities.SessionID) {
	s.l.Lock()
	defer s.l.Unlock()

	delete(s.sessions, sessionID)
}
