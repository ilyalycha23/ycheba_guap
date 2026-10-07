// Copyright 2025-2026 The MathWorks, Inc.

package testutils_test

import (
	"fmt"

	"github.com/matlab/matlab-mcp-server/internal/entities"
	"github.com/matlab/matlab-mcp-server/internal/testutils"
)

func ExampleInspectableLogger() {
	// Arrange your test
	testLogger := testutils.NewInspectableLogger()

	const (
		importantLogToCheck  = "important log"
		keyForImportantLog   = "importantKey"
		valueForImportantLog = "importantValue"

		importantKeyToPersist  = "keyToPersist"
		importantKeyToPersist2 = "keyToPersist2"
		firstLogWithKey        = "log with key"
		secondLogWithKey       = "another log with key"
	)

	// Example function
	act := func(logger entities.Logger) {
		logger.Info("Info log")
		logger.Error("Error log")
		logger.Warn("Warning log")

		logger.With(keyForImportantLog, valueForImportantLog).Debug(importantLogToCheck)

		newLogger := logger.With(importantKeyToPersist, "importantValue")
		newLogger.Debug(firstLogWithKey)
		newLogger.Debug(secondLogWithKey)
	}

	// Act
	act(testLogger)

	// Assert the logs were as you expected
	// Normally this would be with the assert package, but here we use fmt and the example output syntax
	infoLogs := testLogger.InfoLogs()
	fmt.Println("Number of info logs:", len(infoLogs))

	errorLogs := testLogger.ErrorLogs()
	fmt.Println("Number of error logs:", len(errorLogs))

	warnLogs := testLogger.WarnLogs()
	fmt.Println("Number of warn logs:", len(warnLogs))

	debugLogs := testLogger.DebugLogs()

	// We can also check the details of important logs
	fields, ok := debugLogs[importantLogToCheck]
	fmt.Println("Important log found:", ok)
	fmt.Println("Number of fields on the important log:", len(fields))
	fmt.Println("Field found:", fields)

	// The inspectable logger will also correctly handle creating new loggers using `With`
	firstLogFields := debugLogs[firstLogWithKey]
	_, firstKeyFound := firstLogFields[importantKeyToPersist]
	fmt.Println("First log with key found:", firstKeyFound)

	secondLogFields := debugLogs[secondLogWithKey]
	_, secondKeyFound := secondLogFields[importantKeyToPersist]
	fmt.Println("Second log with key found:", secondKeyFound)

	// Output:
	// Number of info logs: 1
	// Number of error logs: 1
	// Number of warn logs: 1
	// Important log found: true
	// Number of fields on the important log: 1
	// Field found: map[importantKey:importantValue]
	// First log with key found: true
	// Second log with key found: true
}
