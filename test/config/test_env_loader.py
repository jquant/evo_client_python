"""Tests for the EnvConfigLoader class."""

import os
import warnings
from unittest.mock import patch

import pytest

from evo_client.config.env_loader import EnvConfigLoader
from evo_client.core.configuration import Configuration


class TestEnvConfigLoader:
    """Test suite for EnvConfigLoader."""

    def setup_method(self):
        """Clean up environment variables before each test."""
        # Store original env vars
        self.original_env = {}
        for key in list(os.environ.keys()):
            if key.startswith("EVO_") or key.startswith("TEST_"):
                self.original_env[key] = os.environ[key]
                del os.environ[key]

    def teardown_method(self):
        """Restore environment variables after each test."""
        # Clean up test env vars
        for key in list(os.environ.keys()):
            if key.startswith("EVO_") or key.startswith("TEST_"):
                del os.environ[key]

        # Restore original env vars
        for key, value in self.original_env.items():
            os.environ[key] = value

    def test_default_env_mappings(self):
        """Test that default environment mappings are correct."""
        expected_mappings = {
            "host": "HOST",
            "username": "USERNAME",
            "password": "PASSWORD",
            "timeout": "TIMEOUT",
            "verify_ssl": "VERIFY_SSL",
            "proxy": "PROXY",
            "ssl_ca_cert": "SSL_CA_CERT",
            "cert_file": "CERT_FILE",
            "key_file": "KEY_FILE",
            "connection_pool_maxsize": "CONNECTION_POOL_MAXSIZE",
            "api_key": "API_KEY",
            "api_key_prefix": "API_KEY_PREFIX",
        }

        assert EnvConfigLoader.DEFAULT_ENV_MAPPINGS == expected_mappings

    def test_load_config_basic_success(self):
        """Test successful loading of basic configuration."""
        # Set required environment variables
        os.environ["EVO_HOST"] = "https://api.example.com"
        os.environ["EVO_USERNAME"] = "test_user"
        os.environ["EVO_PASSWORD"] = "test_pass"

        config = EnvConfigLoader.load_config()

        assert isinstance(config, Configuration)
        assert config.host == "https://api.example.com"
        assert config.username == "test_user"
        assert config.password == "test_pass"

    def test_load_config_all_parameters(self):
        """Test loading configuration with all possible parameters."""
        # Set all environment variables
        env_vars = {
            "EVO_HOST": "https://api.example.com",
            "EVO_USERNAME": "test_user",
            "EVO_PASSWORD": "test_pass",
            "EVO_TIMEOUT": "30.5",
            "EVO_VERIFY_SSL": "false",
            "EVO_PROXY": "http://proxy.example.com:8080",
            "EVO_SSL_CA_CERT": "/path/to/ca.pem",
            "EVO_CERT_FILE": "/path/to/cert.pem",
            "EVO_KEY_FILE": "/path/to/key.pem",
            "EVO_CONNECTION_POOL_MAXSIZE": "50",
            "EVO_API_KEY": "secret_key_123",
            "EVO_API_KEY_PREFIX": "Token",
        }

        for key, value in env_vars.items():
            os.environ[key] = value

        config = EnvConfigLoader.load_config()

        assert config.host == "https://api.example.com"
        assert config.username == "test_user"
        assert config.password == "test_pass"
        assert config.timeout == 30.5
        assert config.verify_ssl is False
        assert config.proxy == "http://proxy.example.com:8080"
        assert config.ssl_ca_cert == "/path/to/ca.pem"
        assert config.cert_file == "/path/to/cert.pem"
        assert config.key_file == "/path/to/key.pem"
        assert config.connection_pool_maxsize == 50
        assert config.api_key == {"ApiKey": "secret_key_123"}
        assert config.api_key_prefix == {"ApiKey": "Token"}

    def test_load_config_custom_prefix(self):
        """Test loading configuration with custom prefix."""
        os.environ["CUSTOM_HOST"] = "https://custom.example.com"
        os.environ["CUSTOM_USERNAME"] = "custom_user"
        os.environ["CUSTOM_PASSWORD"] = "custom_pass"

        config = EnvConfigLoader.load_config(prefix="CUSTOM_")

        assert config.host == "https://custom.example.com"
        assert config.username == "custom_user"
        assert config.password == "custom_pass"

    def test_load_config_missing_required_vars(self):
        """Test error when required variables are missing."""
        # Only set host, missing username and password
        os.environ["EVO_HOST"] = "https://api.example.com"

        with pytest.raises(ValueError, match="Missing required environment variables"):
            EnvConfigLoader.load_config()

    def test_load_config_required_vars_disabled(self):
        """Test loading config with required_vars=False."""
        # Only set host
        os.environ["EVO_HOST"] = "https://api.example.com"

        config = EnvConfigLoader.load_config(required_vars=False)

        assert config.host == "https://api.example.com"
        # Configuration sets default empty strings, not None
        assert config.username == ""
        assert config.password == ""

    def test_load_config_custom_env_mappings(self):
        """Test loading configuration with custom environment mappings."""
        custom_mappings = {
            "host": "CUSTOM_HOST_VAR",
            "username": "CUSTOM_USER_VAR",
            "password": "CUSTOM_PASS_VAR",
        }

        os.environ["EVO_CUSTOM_HOST_VAR"] = "https://custom.example.com"
        os.environ["EVO_CUSTOM_USER_VAR"] = "custom_user"
        os.environ["EVO_CUSTOM_PASS_VAR"] = "custom_pass"

        config = EnvConfigLoader.load_config(env_mappings=custom_mappings)

        assert config.host == "https://custom.example.com"
        assert config.username == "custom_user"
        assert config.password == "custom_pass"

    def test_load_config_fallback_values(self):
        """Test loading configuration with fallback values."""
        fallback_values = {
            "host": "https://fallback.example.com",
            "username": "fallback_user",
            "password": "fallback_pass",
            "timeout": 45.0,
        }

        config = EnvConfigLoader.load_config(
            required_vars=False, fallback_values=fallback_values
        )

        assert config.host == "https://fallback.example.com"
        assert config.username == "fallback_user"
        assert config.password == "fallback_pass"
        assert config.timeout == 45.0

    def test_load_config_env_overrides_fallback(self):
        """Test that environment variables override fallback values."""
        fallback_values = {
            "host": "https://fallback.example.com",
            "username": "fallback_user",
            "password": "fallback_pass",
        }

        # Set only host in environment
        os.environ["EVO_HOST"] = "https://env.example.com"

        config = EnvConfigLoader.load_config(
            required_vars=False, fallback_values=fallback_values
        )

        assert config.host == "https://env.example.com"  # From env
        assert config.username == "fallback_user"  # From fallback
        assert config.password == "fallback_pass"  # From fallback

    def test_load_config_api_key_handling(self):
        """Test special handling of API key and prefix."""
        os.environ["EVO_HOST"] = "https://api.example.com"
        os.environ["EVO_USERNAME"] = "test_user"
        os.environ["EVO_PASSWORD"] = "test_pass"
        os.environ["EVO_API_KEY"] = "secret_key_123"

        config = EnvConfigLoader.load_config()

        assert config.api_key == {"ApiKey": "secret_key_123"}
        assert config.api_key_prefix == {"ApiKey": "Bearer"}  # Default prefix

    def test_load_config_api_key_with_custom_prefix(self):
        """Test API key handling with custom prefix."""
        os.environ["EVO_HOST"] = "https://api.example.com"
        os.environ["EVO_USERNAME"] = "test_user"
        os.environ["EVO_PASSWORD"] = "test_pass"
        os.environ["EVO_API_KEY"] = "secret_key_123"
        os.environ["EVO_API_KEY_PREFIX"] = "Token"

        config = EnvConfigLoader.load_config()

        assert config.api_key == {"ApiKey": "secret_key_123"}
        assert config.api_key_prefix == {"ApiKey": "Token"}

    def test_load_config_invalid_configuration(self):
        """Test error handling when Configuration creation fails."""
        os.environ["EVO_HOST"] = "https://api.example.com"
        os.environ["EVO_USERNAME"] = "test_user"
        os.environ["EVO_PASSWORD"] = "test_pass"

        # Mock Configuration to raise an exception
        with patch(
            "evo_client.config.env_loader.Configuration",
            side_effect=Exception("Invalid config"),
        ):
            with pytest.raises(
                ValueError, match="Invalid configuration from environment"
            ):
                EnvConfigLoader.load_config()

    def test_parse_env_value_boolean_true_values(self):
        """Test parsing boolean environment values (true cases)."""
        true_values = [
            "true",
            "True",
            "TRUE",
            "1",
            "yes",
            "Yes",
            "YES",
            "on",
            "On",
            "ON",
        ]

        for value in true_values:
            result = EnvConfigLoader._parse_env_value("verify_ssl", value)
            assert result is True, f"Failed for value: {value}"

    def test_parse_env_value_boolean_false_values(self):
        """Test parsing boolean environment values (false cases)."""
        false_values = [
            "false",
            "False",
            "FALSE",
            "0",
            "no",
            "No",
            "NO",
            "off",
            "Off",
            "OFF",
            "random",
        ]

        for value in false_values:
            result = EnvConfigLoader._parse_env_value("verify_ssl", value)
            assert result is False, f"Failed for value: {value}"

    def test_parse_env_value_timeout_valid(self):
        """Test parsing valid timeout values."""
        assert EnvConfigLoader._parse_env_value("timeout", "30.5") == 30.5
        assert EnvConfigLoader._parse_env_value("timeout", "60") == 60.0
        assert EnvConfigLoader._parse_env_value("timeout", "0") == 0.0

    def test_parse_env_value_timeout_invalid(self):
        """Test parsing invalid timeout values with warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = EnvConfigLoader._parse_env_value("timeout", "invalid")

            assert result == 60.0  # Default value
            assert len(w) == 1
            assert "Invalid timeout value" in str(w[0].message)

    def test_parse_env_value_connection_pool_maxsize_valid(self):
        """Test parsing valid connection pool maxsize values."""
        assert EnvConfigLoader._parse_env_value("connection_pool_maxsize", "50") == 50
        assert EnvConfigLoader._parse_env_value("connection_pool_maxsize", "1") == 1
        assert EnvConfigLoader._parse_env_value("connection_pool_maxsize", "100") == 100

    def test_parse_env_value_connection_pool_maxsize_invalid(self):
        """Test parsing invalid connection pool maxsize values with warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = EnvConfigLoader._parse_env_value(
                "connection_pool_maxsize", "invalid"
            )

            assert result == 20  # Default value
            assert len(w) == 1
            assert "Invalid connection_pool_maxsize value" in str(w[0].message)

    def test_parse_env_value_string_values(self):
        """Test parsing string values (default case)."""
        assert (
            EnvConfigLoader._parse_env_value("host", "https://api.example.com")
            == "https://api.example.com"
        )
        assert EnvConfigLoader._parse_env_value("username", "test_user") == "test_user"
        assert (
            EnvConfigLoader._parse_env_value("proxy", "http://proxy.com")
            == "http://proxy.com"
        )

    def test_check_env_vars_found(self):
        """Test checking environment variables when they are set."""
        os.environ["EVO_HOST"] = "https://api.example.com"
        os.environ["EVO_USERNAME"] = "test_user"
        os.environ["EVO_TIMEOUT"] = "30"

        found = EnvConfigLoader.check_env_vars()

        expected = {
            "EVO_HOST": "https://api.example.com",
            "EVO_USERNAME": "test_user",
            "EVO_TIMEOUT": "30",
        }
        assert found == expected

    def test_check_env_vars_none_found(self):
        """Test checking environment variables when none are set."""
        found = EnvConfigLoader.check_env_vars()
        assert found == {}

    def test_check_env_vars_custom_prefix(self):
        """Test checking environment variables with custom prefix."""
        # Clean up any existing environment variables first
        for key in list(os.environ.keys()):
            if key.startswith("CUSTOM_"):
                del os.environ[key]

        os.environ["CUSTOM_HOST"] = "https://custom.example.com"
        os.environ["CUSTOM_USERNAME"] = "custom_user"

        found = EnvConfigLoader.check_env_vars(prefix="CUSTOM_")

        expected = {
            "CUSTOM_HOST": "https://custom.example.com",
            "CUSTOM_USERNAME": "custom_user",
        }
        assert found == expected

    def test_get_example_env_file_default_prefix(self):
        """Test generating example .env file with default prefix."""
        content = EnvConfigLoader.get_example_env_file()

        assert "# EVO Client Configuration" in content
        assert "EVO_HOST=https://evo-integracao-api.w12app.com.br" in content
        assert "EVO_USERNAME=your_gym_dns" in content
        assert "EVO_PASSWORD=your_secret_key" in content
        assert "EVO_TIMEOUT=60" in content
        assert "EVO_VERIFY_SSL=true" in content
        assert "# your_api_key_if_using_api_key_auth" in content

    def test_get_example_env_file_custom_prefix(self):
        """Test generating example .env file with custom prefix."""
        content = EnvConfigLoader.get_example_env_file(prefix="CUSTOM_")

        assert "CUSTOM_HOST=https://evo-integracao-api.w12app.com.br" in content
        assert "CUSTOM_USERNAME=your_gym_dns" in content
        assert "CUSTOM_PASSWORD=your_secret_key" in content

    def test_validate_required_vars_success(self):
        """Test successful validation of required variables."""
        os.environ["EVO_HOST"] = "https://api.example.com"
        os.environ["EVO_USERNAME"] = "test_user"
        os.environ["EVO_PASSWORD"] = "test_pass"

        result = EnvConfigLoader.validate_required_vars()
        assert result is True

    def test_validate_required_vars_missing_all(self):
        """Test validation failure when all required variables are missing."""
        with pytest.raises(ValueError, match="Missing required environment variables"):
            EnvConfigLoader.validate_required_vars()

    def test_validate_required_vars_missing_some(self):
        """Test validation failure when some required variables are missing."""
        os.environ["EVO_HOST"] = "https://api.example.com"
        # Missing USERNAME and PASSWORD

        with pytest.raises(ValueError) as exc_info:
            EnvConfigLoader.validate_required_vars()

        error_msg = str(exc_info.value)
        assert "EVO_USERNAME" in error_msg
        assert "EVO_PASSWORD" in error_msg

    def test_validate_required_vars_custom_prefix(self):
        """Test validation with custom prefix."""
        os.environ["CUSTOM_HOST"] = "https://api.example.com"
        os.environ["CUSTOM_USERNAME"] = "test_user"
        os.environ["CUSTOM_PASSWORD"] = "test_pass"

        result = EnvConfigLoader.validate_required_vars(prefix="CUSTOM_")
        assert result is True

    def test_validate_required_vars_custom_prefix_missing(self):
        """Test validation failure with custom prefix when variables are missing."""
        # Clean up any existing CUSTOM_ environment variables
        for key in list(os.environ.keys()):
            if key.startswith("CUSTOM_"):
                del os.environ[key]

        with pytest.raises(ValueError) as exc_info:
            EnvConfigLoader.validate_required_vars(prefix="CUSTOM_")

        error_msg = str(exc_info.value)
        assert "CUSTOM_HOST" in error_msg
        assert "CUSTOM_USERNAME" in error_msg
        assert "CUSTOM_PASSWORD" in error_msg
