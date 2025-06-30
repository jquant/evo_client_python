"""Tests for config presets functionality."""

import multiprocessing
from unittest.mock import patch

import pytest

from evo_client.config.presets import ConfigPresets
from evo_client.core.configuration import Configuration


class TestConfigPresets:
    """Test ConfigPresets static methods."""

    def test_gym_production(self):
        """Test gym production configuration preset."""
        config = ConfigPresets.gym_production()

        assert isinstance(config, Configuration)
        assert config.host == "https://evo-integracao-api.w12app.com.br"
        assert config.timeout == 60.0
        assert config.verify_ssl is True
        assert config.connection_pool_maxsize == 20
        assert "Production" in config.default_headers["User-Agent"]
        assert config.default_headers["Accept"] == "application/json"
        assert config.default_headers["Content-Type"] == "application/json"

    def test_gym_development(self):
        """Test gym development configuration preset."""
        config = ConfigPresets.gym_development()

        assert isinstance(config, Configuration)
        assert config.host == "https://evo-integracao-api.w12app.com.br"
        assert config.username == "demo"
        assert config.password == "demo"
        assert config.timeout == 120.0
        assert config.verify_ssl is False
        assert config.connection_pool_maxsize == 5
        assert "Development" in config.default_headers["User-Agent"]
        assert config.default_headers["Accept"] == "application/json"
        assert config.default_headers["Content-Type"] == "application/json"

    def test_high_performance(self):
        """Test high performance configuration preset."""
        config = ConfigPresets.high_performance()

        assert isinstance(config, Configuration)
        assert config.host == "https://evo-integracao-api.w12app.com.br"
        assert config.timeout == 90.0
        assert config.verify_ssl is True
        assert config.connection_pool_maxsize == multiprocessing.cpu_count() * 10
        assert "HighPerformance" in config.default_headers["User-Agent"]
        assert config.default_headers["Accept"] == "application/json"
        assert config.default_headers["Content-Type"] == "application/json"
        assert config.default_headers["Connection"] == "keep-alive"

    @patch("multiprocessing.cpu_count", return_value=4)
    def test_high_performance_with_mocked_cpu_count(self, mock_cpu_count):
        """Test high performance preset with mocked CPU count."""
        config = ConfigPresets.high_performance()

        assert config.connection_pool_maxsize == 40  # 4 * 10
        mock_cpu_count.assert_called_once()

    def test_low_latency(self):
        """Test low latency configuration preset."""
        config = ConfigPresets.low_latency()

        assert isinstance(config, Configuration)
        assert config.host == "https://evo-integracao-api.w12app.com.br"
        assert config.timeout == 15.0
        assert config.verify_ssl is True
        assert config.connection_pool_maxsize == 5
        assert "LowLatency" in config.default_headers["User-Agent"]
        assert config.default_headers["Accept"] == "application/json"
        assert config.default_headers["Content-Type"] == "application/json"
        assert config.default_headers["Cache-Control"] == "no-cache"

    def test_testing(self):
        """Test testing configuration preset."""
        config = ConfigPresets.testing()

        assert isinstance(config, Configuration)
        assert config.host == "https://evo-integracao-api.w12app.com.br"
        assert config.username == "test"
        assert config.password == "test"
        assert config.timeout == 30.0
        assert config.verify_ssl is False
        assert config.connection_pool_maxsize == 1
        assert "Testing" in config.default_headers["User-Agent"]
        assert config.default_headers["Accept"] == "application/json"
        assert config.default_headers["Content-Type"] == "application/json"

    def test_custom_host_production(self):
        """Test custom host with production preset."""
        custom_host = "https://my-custom-api.example.com"
        config = ConfigPresets.custom_host(custom_host, "production")

        assert isinstance(config, Configuration)
        assert config.host == custom_host
        assert config.timeout == 60.0  # From production preset
        assert config.verify_ssl is True
        assert config.connection_pool_maxsize == 20
        assert "Production" in config.default_headers["User-Agent"]

    def test_custom_host_development(self):
        """Test custom host with development preset."""
        custom_host = "https://dev-api.example.com"
        config = ConfigPresets.custom_host(custom_host, "development")

        assert isinstance(config, Configuration)
        assert config.host == custom_host
        assert config.username == "demo"  # From development preset
        assert config.password == "demo"
        assert config.timeout == 120.0
        assert config.verify_ssl is False
        assert config.connection_pool_maxsize == 5

    def test_custom_host_high_performance(self):
        """Test custom host with high performance preset."""
        custom_host = "https://perf-api.example.com"
        config = ConfigPresets.custom_host(custom_host, "high_performance")

        assert isinstance(config, Configuration)
        assert config.host == custom_host
        assert config.timeout == 90.0  # From high performance preset
        assert config.connection_pool_maxsize == multiprocessing.cpu_count() * 10

    def test_custom_host_low_latency(self):
        """Test custom host with low latency preset."""
        custom_host = "https://fast-api.example.com"
        config = ConfigPresets.custom_host(custom_host, "low_latency")

        assert isinstance(config, Configuration)
        assert config.host == custom_host
        assert config.timeout == 15.0  # From low latency preset
        assert config.connection_pool_maxsize == 5

    def test_custom_host_testing(self):
        """Test custom host with testing preset."""
        custom_host = "https://test-api.example.com"
        config = ConfigPresets.custom_host(custom_host, "testing")

        assert isinstance(config, Configuration)
        assert config.host == custom_host
        assert config.username == "test"  # From testing preset
        assert config.password == "test"
        assert config.timeout == 30.0
        assert config.connection_pool_maxsize == 1

    def test_custom_host_default_preset(self):
        """Test custom host with default preset type (production)."""
        custom_host = "https://default-api.example.com"
        config = ConfigPresets.custom_host(custom_host)

        assert isinstance(config, Configuration)
        assert config.host == custom_host
        assert config.timeout == 60.0  # Default to production
        assert config.verify_ssl is True

    def test_custom_host_invalid_preset_type(self):
        """Test custom host with invalid preset type raises ValueError."""
        with pytest.raises(ValueError, match="Unknown preset type: invalid"):
            ConfigPresets.custom_host("https://api.example.com", "invalid")

    def test_with_proxy_production(self):
        """Test proxy configuration with production preset."""
        proxy_url = "http://proxy.company.com:8080"
        config = ConfigPresets.with_proxy(proxy_url, "production")

        assert isinstance(config, Configuration)
        assert config.proxy == proxy_url
        assert config.timeout == 60.0  # From production preset
        assert config.verify_ssl is True
        assert config.connection_pool_maxsize == 20

    def test_with_proxy_development(self):
        """Test proxy configuration with development preset."""
        proxy_url = "http://dev-proxy.company.com:8080"
        config = ConfigPresets.with_proxy(proxy_url, "development")

        assert isinstance(config, Configuration)
        assert config.proxy == proxy_url
        assert config.username == "demo"  # From development preset
        assert config.password == "demo"
        assert config.timeout == 120.0

    def test_with_proxy_high_performance(self):
        """Test proxy configuration with high performance preset."""
        proxy_url = "http://fast-proxy.company.com:8080"
        config = ConfigPresets.with_proxy(proxy_url, "high_performance")

        assert isinstance(config, Configuration)
        assert config.proxy == proxy_url
        assert config.timeout == 90.0  # From high performance preset
        assert config.connection_pool_maxsize == multiprocessing.cpu_count() * 10

    def test_with_proxy_low_latency(self):
        """Test proxy configuration with low latency preset."""
        proxy_url = "http://local-proxy.company.com:8080"
        config = ConfigPresets.with_proxy(proxy_url, "low_latency")

        assert isinstance(config, Configuration)
        assert config.proxy == proxy_url
        assert config.timeout == 15.0  # From low latency preset
        assert config.connection_pool_maxsize == 5

    def test_with_proxy_testing(self):
        """Test proxy configuration with testing preset."""
        proxy_url = "http://test-proxy.company.com:8080"
        config = ConfigPresets.with_proxy(proxy_url, "testing")

        assert isinstance(config, Configuration)
        assert config.proxy == proxy_url
        assert config.username == "test"  # From testing preset
        assert config.password == "test"
        assert config.timeout == 30.0

    def test_with_proxy_default_preset(self):
        """Test proxy configuration with default preset type (production)."""
        proxy_url = "http://default-proxy.company.com:8080"
        config = ConfigPresets.with_proxy(proxy_url)

        assert isinstance(config, Configuration)
        assert config.proxy == proxy_url
        assert config.timeout == 60.0  # Default to production
        assert config.verify_ssl is True

    def test_with_proxy_invalid_preset_type(self):
        """Test proxy configuration with invalid preset type raises ValueError."""
        with pytest.raises(ValueError, match="Unknown preset type: unknown"):
            ConfigPresets.with_proxy("http://proxy.com:8080", "unknown")

    def test_list_presets(self):
        """Test listing all available presets."""
        presets = ConfigPresets.list_presets()

        assert isinstance(presets, dict)
        assert len(presets) == 7

        # Check all expected presets are present
        expected_presets = {
            "gym_production",
            "gym_development",
            "high_performance",
            "low_latency",
            "testing",
            "custom_host",
            "with_proxy",
        }
        assert set(presets.keys()) == expected_presets

        # Check descriptions are strings
        for name, description in presets.items():
            assert isinstance(description, str)
            assert len(description) > 0

        # Check specific descriptions
        assert "Production configuration" in presets["gym_production"]
        assert "Development configuration" in presets["gym_development"]
        assert "High-throughput configuration" in presets["high_performance"]
        assert "Minimal response time" in presets["low_latency"]
        assert "Testing-friendly configuration" in presets["testing"]
        assert "Custom host configuration" in presets["custom_host"]
        assert "Proxy-enabled configuration" in presets["with_proxy"]


class TestConfigPresetsIntegration:
    """Test integration scenarios with presets."""

    def test_all_presets_return_valid_configurations(self):
        """Test that all basic presets return valid Configuration objects."""
        basic_presets = [
            ConfigPresets.gym_production,
            ConfigPresets.gym_development,
            ConfigPresets.high_performance,
            ConfigPresets.low_latency,
            ConfigPresets.testing,
        ]

        for preset_func in basic_presets:
            config = preset_func()
            assert isinstance(config, Configuration)
            assert config.host  # Should have a host
            assert config.timeout > 0  # Should have positive timeout
            assert isinstance(config.verify_ssl, bool)
            assert config.connection_pool_maxsize > 0
            assert isinstance(config.default_headers, dict)

    def test_preset_customization(self):
        """Test that preset configurations can be customized after creation."""
        config = ConfigPresets.gym_production()

        # Customize the config
        config.username = "custom_user"
        config.password = "custom_pass"
        config.timeout = 45.0

        assert config.username == "custom_user"
        assert config.password == "custom_pass"
        assert config.timeout == 45.0
        # Original preset values should remain for other fields
        assert config.verify_ssl is True
        assert config.connection_pool_maxsize == 20

    def test_preset_inheritance(self):
        """Test that custom_host and with_proxy properly inherit from base presets."""
        # Test custom host inherits all properties except host
        base_config = ConfigPresets.gym_development()
        custom_config = ConfigPresets.custom_host(
            "https://custom.example.com", "development"
        )

        assert custom_config.host != base_config.host
        assert custom_config.username == base_config.username
        assert custom_config.password == base_config.password
        assert custom_config.timeout == base_config.timeout
        assert custom_config.verify_ssl == base_config.verify_ssl
        assert (
            custom_config.connection_pool_maxsize == base_config.connection_pool_maxsize
        )

        # Test proxy config inherits all properties except proxy
        proxy_config = ConfigPresets.with_proxy("http://proxy.com:8080", "development")

        assert proxy_config.proxy != base_config.proxy
        assert proxy_config.username == base_config.username
        assert proxy_config.password == base_config.password
        assert proxy_config.timeout == base_config.timeout
        assert proxy_config.verify_ssl == base_config.verify_ssl

    def test_headers_consistency(self):
        """Test that all presets have consistent header structure."""
        configs = [
            ConfigPresets.gym_production(),
            ConfigPresets.gym_development(),
            ConfigPresets.high_performance(),
            ConfigPresets.low_latency(),
            ConfigPresets.testing(),
        ]

        for config in configs:
            headers = config.default_headers
            assert "User-Agent" in headers
            assert "Accept" in headers
            assert "Content-Type" in headers
            assert headers["Accept"] == "application/json"
            assert headers["Content-Type"] == "application/json"
            assert "EVO-Client-Python" in headers["User-Agent"]
