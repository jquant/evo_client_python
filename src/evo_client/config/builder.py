"""
Configuration Builder for EVO Client
====================================

Provides easy-to-use factory methods for creating configurations that work
seamlessly with both sync and async EVO clients.
"""

from typing import Dict

from ..core.configuration import Configuration


class ConfigBuilder:
    """Builder class for creating EVO Client configurations."""

    @classmethod
    def from_env(
        cls, prefix: str = "EVO_", required_vars: bool = True
    ) -> Configuration:
        """
        Create configuration from environment variables.

        Args:
            prefix: Prefix for environment variables (default: "EVO_")
            required_vars: Whether to require essential variables

        Environment Variables:
            EVO_HOST: API host URL
            EVO_USERNAME: API username
            EVO_PASSWORD: API password
            EVO_TIMEOUT: Request timeout in seconds
            EVO_VERIFY_SSL: Whether to verify SSL certificates
            EVO_PROXY: Proxy URL if needed

        Returns:
            Configuration object ready for sync/async clients

        Example:
            ```python
            # Set environment variables
            # export EVO_HOST="https://api.evo.com"
            # export EVO_USERNAME="your_username"
            # export EVO_PASSWORD="your_password"

            config = ConfigBuilder.from_env()

            # Use with any client
            from evo_client import SyncApiClient, AsyncApiClient
            with SyncApiClient(config) as client:
                pass
            ```
        """
        from .env_loader import EnvConfigLoader

        return EnvConfigLoader.load_config(prefix=prefix, required_vars=required_vars)

    @classmethod
    def basic_auth(
        cls,
        host: str,
        username: str,
        password: str,
        timeout: float = 60.0,
        verify_ssl: bool = True,
        **kwargs,
    ) -> Configuration:
        """
        Create configuration with basic authentication.

        Args:
            host: API host URL
            username: API username
            password: API password
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            **kwargs: Additional configuration options

        Returns:
            Configuration object ready for sync/async clients

        Example:
            ```python
            config = ConfigBuilder.basic_auth(
                host="https://api.evo.com",
                username="your_username",
                password="your_password"
            )

            # Works with both sync and async
            async with AsyncApiClient(config) as client:
                members_api = AsyncMembersApi(client)
                members = await members_api.get_members()
            ```
        """
        return Configuration(
            host=host,
            username=username,
            password=password,
            timeout=timeout,
            verify_ssl=verify_ssl,
            **kwargs,
        )

    @classmethod
    def api_key_auth(
        cls,
        host: str,
        api_key: str,
        api_key_prefix: str = "Bearer",
        timeout: float = 60.0,
        verify_ssl: bool = True,
        **kwargs,
    ) -> Configuration:
        """
        Create configuration with API key authentication.

        Args:
            host: API host URL
            api_key: API key for authentication
            api_key_prefix: Prefix for API key (default: "Bearer")
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
            **kwargs: Additional configuration options

        Returns:
            Configuration object ready for sync/async clients

        Example:
            ```python
            config = ConfigBuilder.api_key_auth(
                host="https://api.evo.com",
                api_key="your_api_key"
            )

            with SyncApiClient(config) as client:
                sales_api = SyncSalesApi(client)
                sales = sales_api.get_sales()
            ```
        """
        return Configuration(
            host=host,
            api_key={"ApiKey": api_key},
            api_key_prefix={"ApiKey": api_key_prefix},
            timeout=timeout,
            verify_ssl=verify_ssl,
            **kwargs,
        )

    @classmethod
    def development(
        cls,
        host: str = "https://evo-integracao-api.w12app.com.br",
        username: str = "demo",
        password: str = "demo",
        timeout: float = 120.0,
        verify_ssl: bool = False,
        **kwargs,
    ) -> Configuration:
        """
        Create development-friendly configuration.

        Args:
            host: API host URL (default: EVO integration host)
            username: API username (default: "demo")
            password: API password (default: "demo")
            timeout: Request timeout in seconds (longer for debugging)
            verify_ssl: Whether to verify SSL certificates (disabled for dev)
            **kwargs: Additional configuration options

        Returns:
            Configuration object optimized for development

        Example:
            ```python
            # Quick setup for development
            config = ConfigBuilder.development()

            # Ready to use for testing
            async with AsyncApiClient(config) as client:
                # Test your code
                pass
            ```
        """
        return Configuration(
            host=host,
            username=username,
            password=password,
            timeout=timeout,
            verify_ssl=verify_ssl,
            **kwargs,
        )

    @classmethod
    def production(
        cls,
        host: str,
        username: str,
        password: str,
        timeout: float = 60.0,
        verify_ssl: bool = True,
        connection_pool_maxsize: int = 20,
        **kwargs,
    ) -> Configuration:
        """
        Create production-optimized configuration.

        Args:
            host: API host URL
            username: API username
            password: API password
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates (enabled for security)
            connection_pool_maxsize: Max connections in pool
            **kwargs: Additional configuration options

        Returns:
            Configuration object optimized for production

        Example:
            ```python
            config = ConfigBuilder.production(
                host="https://api.evo.com",
                username=os.getenv("EVO_USERNAME"),
                password=os.getenv("EVO_PASSWORD")
            )

            # Production-ready configuration
            with SyncApiClient(config) as client:
                # Production code
                pass
            ```
        """
        return Configuration(
            host=host,
            username=username,
            password=password,
            timeout=timeout,
            verify_ssl=verify_ssl,
            connection_pool_maxsize=connection_pool_maxsize,
            **kwargs,
        )


class QuickConfig:
    """Quick configuration shortcuts for common scenarios."""

    @staticmethod
    def gym_basic(gym_dns: str, secret_key: str) -> Configuration:
        """
        Quick configuration for gym with DNS and secret key.

        Args:
            gym_dns: Your gym's DNS name
            secret_key: Your gym's secret key

        Returns:
            Ready-to-use configuration

        Example:
            ```python
            config = QuickConfig.gym_basic("mygym", "secret123")

            with SyncApiClient(config) as client:
                members_api = SyncMembersApi(client)
                members = members_api.get_members()
            ```
        """
        return ConfigBuilder.basic_auth(
            host="https://evo-integracao-api.w12app.com.br",
            username=gym_dns,
            password=secret_key,
        )

    @staticmethod
    def local_dev() -> Configuration:
        """
        Quick configuration for local development.

        Returns:
            Development-friendly configuration
        """
        return ConfigBuilder.development()

    @staticmethod
    def from_dict(config_dict: Dict) -> Configuration:
        """
        Create configuration from dictionary.

        Args:
            config_dict: Dictionary with configuration values

        Returns:
            Configuration object

        Example:
            ```python
            config_data = {
                "host": "https://api.evo.com",
                "username": "user",
                "password": "pass"
            }
            config = QuickConfig.from_dict(config_data)
            ```
        """
        return Configuration(**config_dict)
