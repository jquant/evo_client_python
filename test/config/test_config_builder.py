"""Tests for config builder functionality."""

from unittest.mock import Mock, patch

import pytest

from evo_client.config.builder import ConfigBuilder, QuickConfig
from evo_client.core.configuration import Configuration


class TestConfigBuilder:
    """Test ConfigBuilder class methods."""

    def test_from_env_default_params(self):
        """Test from_env with default parameters."""
        mock_config = Configuration(
            host="https://test.com", username="user", password="pass"
        )

        with patch("evo_client.config.env_loader.EnvConfigLoader") as mock_loader:
            mock_loader.load_config.return_value = mock_config

            result = ConfigBuilder.from_env()

            mock_loader.load_config.assert_called_once_with(
                prefix="EVO_", required_vars=True
            )
            assert result == mock_config

    def test_from_env_custom_params(self):
        """Test from_env with custom parameters."""
        mock_config = Configuration(
            host="https://test.com", username="user", password="pass"
        )

        with patch("evo_client.config.env_loader.EnvConfigLoader") as mock_loader:
            mock_loader.load_config.return_value = mock_config

            result = ConfigBuilder.from_env(prefix="CUSTOM_", required_vars=False)

            mock_loader.load_config.assert_called_once_with(
                prefix="CUSTOM_", required_vars=False
            )
            assert result == mock_config

    def test_basic_auth(self):
        """Test basic authentication configuration."""
        config = ConfigBuilder.basic_auth(
            host="https://api.example.com",
            username="testuser",
            password="testpass",
            timeout=30.0,
            verify_ssl=False,
        )

        assert isinstance(config, Configuration)
        assert config.host == "https://api.example.com"
        assert config.username == "testuser"
        assert config.password == "testpass"
        assert config.timeout == 30.0
        assert config.verify_ssl is False

    def test_basic_auth_with_kwargs(self):
        """Test basic authentication configuration with additional kwargs."""
        config = ConfigBuilder.basic_auth(
            host="https://api.example.com",
            username="testuser",
            password="testpass",
            custom_param="custom_value",
        )

        assert isinstance(config, Configuration)
        assert config.host == "https://api.example.com"
        assert config.username == "testuser"
        assert config.password == "testpass"
        # Default values
        assert config.timeout == 60.0
        assert config.verify_ssl is True

    def test_api_key_auth(self):
        """Test API key authentication configuration."""
        config = ConfigBuilder.api_key_auth(
            host="https://api.example.com",
            api_key="test_api_key",
            api_key_prefix="Token",
            timeout=45.0,
            verify_ssl=False,
        )

        assert isinstance(config, Configuration)
        assert config.host == "https://api.example.com"
        assert config.api_key == {"ApiKey": "test_api_key"}
        assert config.api_key_prefix == {"ApiKey": "Token"}
        assert config.timeout == 45.0
        assert config.verify_ssl is False

    def test_api_key_auth_default_prefix(self):
        """Test API key authentication with default prefix."""
        config = ConfigBuilder.api_key_auth(
            host="https://api.example.com", api_key="test_api_key"
        )

        assert isinstance(config, Configuration)
        assert config.api_key == {"ApiKey": "test_api_key"}
        assert config.api_key_prefix == {"ApiKey": "Bearer"}
        # Default values
        assert config.timeout == 60.0
        assert config.verify_ssl is True

    def test_development(self):
        """Test development configuration."""
        config = ConfigBuilder.development()

        assert isinstance(config, Configuration)
        assert config.host == "https://evo-integracao-api.w12app.com.br"
        assert config.username == "demo"
        assert config.password == "demo"
        assert config.timeout == 120.0
        assert config.verify_ssl is False

    def test_development_custom_params(self):
        """Test development configuration with custom parameters."""
        config = ConfigBuilder.development(
            host="https://custom-dev.com",
            username="dev_user",
            password="dev_pass",
            timeout=180.0,
            verify_ssl=True,
        )

        assert isinstance(config, Configuration)
        assert config.host == "https://custom-dev.com"
        assert config.username == "dev_user"
        assert config.password == "dev_pass"
        assert config.timeout == 180.0
        assert config.verify_ssl is True

    def test_production(self):
        """Test production configuration."""
        config = ConfigBuilder.production(
            host="https://api.production.com",
            username="prod_user",
            password="prod_pass",
        )

        assert isinstance(config, Configuration)
        assert config.host == "https://api.production.com"
        assert config.username == "prod_user"
        assert config.password == "prod_pass"
        # Default values
        assert config.timeout == 60.0
        assert config.verify_ssl is True
        assert config.connection_pool_maxsize == 20

    def test_production_custom_params(self):
        """Test production configuration with custom parameters."""
        config = ConfigBuilder.production(
            host="https://api.production.com",
            username="prod_user",
            password="prod_pass",
            timeout=90.0,
            verify_ssl=False,
            connection_pool_maxsize=50,
        )

        assert isinstance(config, Configuration)
        assert config.host == "https://api.production.com"
        assert config.username == "prod_user"
        assert config.password == "prod_pass"
        assert config.timeout == 90.0
        assert config.verify_ssl is False
        assert config.connection_pool_maxsize == 50


class TestQuickConfig:
    """Test QuickConfig class methods."""

    def test_gym_basic(self):
        """Test gym basic configuration."""
        config = QuickConfig.gym_basic("mygym", "secret123")

        assert isinstance(config, Configuration)
        assert config.host == "https://evo-integracao-api.w12app.com.br"
        assert config.username == "mygym"
        assert config.password == "secret123"

    def test_local_dev(self):
        """Test local development configuration."""
        config = QuickConfig.local_dev()

        assert isinstance(config, Configuration)
        assert config.host == "https://evo-integracao-api.w12app.com.br"
        assert config.username == "demo"
        assert config.password == "demo"
        assert config.timeout == 120.0
        assert config.verify_ssl is False

    def test_from_dict(self):
        """Test configuration from dictionary."""
        config_dict = {
            "host": "https://api.test.com",
            "username": "dict_user",
            "password": "dict_pass",
            "timeout": 75.0,
            "verify_ssl": True,
        }

        config = QuickConfig.from_dict(config_dict)

        assert isinstance(config, Configuration)
        assert config.host == "https://api.test.com"
        assert config.username == "dict_user"
        assert config.password == "dict_pass"
        assert config.timeout == 75.0
        assert config.verify_ssl is True

    def test_from_dict_minimal(self):
        """Test configuration from minimal dictionary."""
        config_dict = {
            "host": "https://minimal.com",
            "username": "user",
            "password": "pass",
        }

        config = QuickConfig.from_dict(config_dict)

        assert isinstance(config, Configuration)
        assert config.host == "https://minimal.com"
        assert config.username == "user"
        assert config.password == "pass"
