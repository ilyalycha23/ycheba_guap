// Copyright 2026 The MathWorks, Inc.

package main

type DataService struct {
	prefix string
}

func NewDataService(prefix string) *DataService {
	return &DataService{
		prefix: prefix,
	}
}

func (s *DataService) GetData(name string) string {
	return s.prefix + " " + name
}
