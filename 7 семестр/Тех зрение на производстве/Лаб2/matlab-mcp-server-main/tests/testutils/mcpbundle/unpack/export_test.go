// Copyright 2026 The MathWorks, Inc.

package unpack

func NewUnpackerForTest(fs FileSystem) *Unpacker {
	return newUnpacker(fs)
}
