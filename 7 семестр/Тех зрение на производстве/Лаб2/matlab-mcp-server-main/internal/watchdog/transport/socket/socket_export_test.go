// Copyright 2025-2026 The MathWorks, Inc.

package socket

func NewSocket(
	directory Directory,
	osLayer OSLayer,
) (Socket, error) {
	return newSocket(
		directory,
		osLayer,
	)
}
