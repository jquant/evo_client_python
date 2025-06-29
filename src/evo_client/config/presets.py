"""
Configuration Presets for EVO Client
====================================

Pre-configured settings for common EVO Client usage scenarios.
Makes it easy to get started with sensible defaults.
"""

from typing import Dict

from ..core.configuration import Configuration


class ConfigPresets:
    """Pre-configured settings for common scenarios."""

    @staticmethod
    def gym_production() -> Configuration:
        """
        Production configuration for gym operations.

        Optimized for reliability, security, and performance in production.

        Returns:
            Production-optimized configuration

        Features:
            - SSL verification enabled
            - Optimized timeouts
            - Connection pooling
            - Security-focused defaults

        Example:
            ```python
            config = ConfigPresets.gym_production()
            config.username = "your_gym_dns"
            config.password = "your_secret_key"

            with SyncApiClient(config) as client:
                # Production-ready client
                pass
            ```
        """
        return Configuration(
            host="https://evo-integracao-api.w12app.com.br",
            timeout=60.0,
            verify_ssl=True,
            connection_pool_maxsize=20,
            default_headers={
                "User-Agent": "EVO-Client-Python/1.0.0 (Production)",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

    @staticmethod
    def gym_development() -> Configuration:
        """
        Development configuration for gym operations.

        Optimized for debugging and development with relaxed security.

        Returns:
            Development-friendly configuration

        Features:
            - SSL verification disabled (for local dev)
            - Extended timeouts (for debugging)
            - Detailed headers
            - Development defaults

        Example:
            ```python
            config = ConfigPresets.gym_development()
            config.username = "demo"
            config.password = "demo"

            async with AsyncApiClient(config) as client:
                # Development-ready client
                pass
            ```
        """
        return Configuration(
            host="https://evo-integracao-api.w12app.com.br",
            username="demo",
            password="demo",
            timeout=120.0,
            verify_ssl=False,
            connection_pool_maxsize=5,
            default_headers={
                "User-Agent": "EVO-Client-Python/1.0.0 (Development)",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

    @staticmethod
    def high_performance() -> Configuration:
        """
        High-performance configuration for heavy workloads.

        Optimized for maximum throughput and concurrent operations.

        Returns:
            High-performance configuration

        Features:
            - Large connection pool
            - Optimized timeouts
            - Bulk operation support
            - Performance headers

        Example:
            ```python
            config = ConfigPresets.high_performance()
            config.username = "your_gym_dns"
            config.password = "your_secret_key"

            # Perfect for bulk operations
            async with AsyncApiClient(config) as client:
                # High-performance async operations
                members_api = AsyncMembersApi(client)

                # Process large datasets efficiently
                members = await members_api.get_members(take=1000)
            ```
        """
        import multiprocessing

        return Configuration(
            host="https://evo-integracao-api.w12app.com.br",
            timeout=90.0,
            verify_ssl=True,
            connection_pool_maxsize=multiprocessing.cpu_count() * 10,
            default_headers={
                "User-Agent": "EVO-Client-Python/1.0.0 (HighPerformance)",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Connection": "keep-alive",
            },
        )

    @staticmethod
    def low_latency() -> Configuration:
        """
        Low-latency configuration for time-sensitive operations.

        Optimized for minimal response times and quick operations.

        Returns:
            Low-latency configuration

        Features:
            - Short timeouts
            - Minimal connection pool
            - Optimized headers
            - Fast fail settings

        Example:
            ```python
            config = ConfigPresets.low_latency()
            config.username = "your_gym_dns"
            config.password = "your_secret_key"

            with SyncApiClient(config) as client:
                # Fast, responsive operations
                sales_api = SyncSalesApi(client)
                recent_sales = sales_api.get_sales(take=10)
            ```
        """
        return Configuration(
            host="https://evo-integracao-api.w12app.com.br",
            timeout=15.0,
            verify_ssl=True,
            connection_pool_maxsize=5,
            default_headers={
                "User-Agent": "EVO-Client-Python/1.0.0 (LowLatency)",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Cache-Control": "no-cache",
            },
        )

    @staticmethod
    def testing() -> Configuration:
        """
        Testing configuration for unit tests and integration tests.

        Optimized for test reliability and isolation.

        Returns:
            Testing-friendly configuration

        Features:
            - Predictable timeouts
            - Isolated settings
            - Test-friendly defaults
            - Mock-ready configuration

        Example:
            ```python
            # In your test files
            config = ConfigPresets.testing()
            config.username = "test_user"
            config.password = "test_pass"

            def test_members_api():
                with SyncApiClient(config) as client:
                    members_api = SyncMembersApi(client)
                    # Test your API calls
                    pass
            ```
        """
        return Configuration(
            host="https://evo-integracao-api.w12app.com.br",
            username="test",
            password="test",
            timeout=30.0,
            verify_ssl=False,
            connection_pool_maxsize=1,
            default_headers={
                "User-Agent": "EVO-Client-Python/1.0.0 (Testing)",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

    @staticmethod
    def custom_host(host: str, preset_type: str = "production") -> Configuration:
        """
        Custom host configuration based on existing preset.

        Args:
            host: Custom API host URL
            preset_type: Base preset type ("production", "development", etc.)

        Returns:
            Configuration with custom host

        Example:
            ```python
            # Use custom host with production settings
            config = ConfigPresets.custom_host(
                host="https://my-custom-api.com",
                preset_type="production"
            )
            config.username = "user"
            config.password = "pass"
            ```
        """
        preset_map = {
            "production": ConfigPresets.gym_production,
            "development": ConfigPresets.gym_development,
            "high_performance": ConfigPresets.high_performance,
            "low_latency": ConfigPresets.low_latency,
            "testing": ConfigPresets.testing,
        }

        if preset_type not in preset_map:
            raise ValueError(f"Unknown preset type: {preset_type}")

        config = preset_map[preset_type]()
        config.host = host
        return config

    @staticmethod
    def with_proxy(proxy_url: str, preset_type: str = "production") -> Configuration:
        """
        Configuration with proxy settings based on existing preset.

        Args:
            proxy_url: Proxy URL (e.g., "http://proxy.company.com:8080")
            preset_type: Base preset type

        Returns:
            Configuration with proxy settings

        Example:
            ```python
            config = ConfigPresets.with_proxy(
                proxy_url="http://proxy.company.com:8080",
                preset_type="production"
            )
            config.username = "user"
            config.password = "pass"
            ```
        """
        preset_map = {
            "production": ConfigPresets.gym_production,
            "development": ConfigPresets.gym_development,
            "high_performance": ConfigPresets.high_performance,
            "low_latency": ConfigPresets.low_latency,
            "testing": ConfigPresets.testing,
        }

        if preset_type not in preset_map:
            raise ValueError(f"Unknown preset type: {preset_type}")

        config = preset_map[preset_type]()
        config.proxy = proxy_url
        return config

    @staticmethod
    def list_presets() -> Dict[str, str]:
        """
        List all available configuration presets.

        Returns:
            Dictionary mapping preset names to descriptions

        Example:
            ```python
            presets = ConfigPresets.list_presets()
            for name, description in presets.items():
                print(f"{name}: {description}")
            ```
        """
        return {
            "gym_production": "Production configuration for gym operations",
            "gym_development": "Development configuration with relaxed security",
            "high_performance": "High-throughput configuration for bulk operations",
            "low_latency": "Minimal response time configuration",
            "testing": "Testing-friendly configuration for unit tests",
            "custom_host": "Custom host configuration with preset base",
            "with_proxy": "Proxy-enabled configuration with preset base",
        }
