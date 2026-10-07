classdef DefaultSecureGeneratorTest < matlab.unittest.TestCase
%DefaultSecureGeneratorTest Integration tests for DefaultSecureGenerator
%   These tests verify real .NET crypto calls on Windows and real
%   /dev/urandom reads on Unix. They require actual OS resources.

    % Copyright 2026 The MathWorks, Inc.

    properties (Constant, Access = private)
        ExpectedKeySize(1,1) uint8 = 24
    end

    methods (Test)
        function testDefaultSecureGenerator_GenerateKey_ProducesValidKey(testCase)
            % Arrange
            generator = mcpserver.internal.connector.internal.apikeymanager.internal.securegen.DefaultSecureGenerator();

            % Act
            key = generator.generateKey();

            % Assert
            testCase.verifyTrue(strlength(key) == 2*testCase.ExpectedKeySize, ...
                sprintf("Key should be %d hex characters (%d bytes)", 2*testCase.ExpectedKeySize, testCase.ExpectedKeySize));
            testCase.verifyTrue( ...
                ~isempty(regexp(key, sprintf("^[0-9a-f]{%d}$", 2*testCase.ExpectedKeySize), "once")), ...
                "Key should contain only lowercase hexadecimal characters");
        end

        function testDefaultSecureGenerator_GenerateKey_ProducesUniqueKeys(testCase)
            % Arrange
            generator = mcpserver.internal.connector.internal.apikeymanager.internal.securegen.DefaultSecureGenerator();

            % Act
            key1 = generator.generateKey();
            key2 = generator.generateKey();

            % Assert
            testCase.verifyNotEqual(key1, key2, ...
                "Two generated keys should be different (cryptographically random)");
        end
    end

end
