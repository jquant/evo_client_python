"""
Environment Variable Configuration Loader
=========================================

Automatically loads EVO Client configuration from environment variables,
making it easy to configure applications through environment settings.
"""

import os
from typing import Any, Dict, Optional
from warnings import warn

from ..core.configuration import Configuration


class EnvConfigLoader:
    """Loads configuration from environment variables."""

    # Default environment variable mappings
    DEFAULT_ENV_MAPPINGS = {
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

    @classmethod
    def load_config(
        cls,
        prefix: str = "EVO_",
        required_vars: bool = True,
        env_mappings: Optional[Dict[str, str]] = None,
        fallback_values: Optional[Dict[str, Any]] = None,
    ) -> Configuration:
        """
        Load configuration from environment variables.

        Args:
            prefix: Prefix for environment variables (default: "EVO_")
            required_vars: Whether to require essential variables
            env_mappings: Custom environment variable mappings
            fallback_values: Fallback values if env vars not found

        Returns:
            Configuration object loaded from environment

        Environment Variables (with EVO_ prefix):
            EVO_HOST: API host URL
            EVO_USERNAME: API username
            EVO_PASSWORD: API password
            EVO_TIMEOUT: Request timeout in seconds
            EVO_VERIFY_SSL: Whether to verify SSL (true/false)
            EVO_PROXY: Proxy URL if needed
            EVO_SSL_CA_CERT: Path to CA certificate file
            EVO_CERT_FILE: Path to client certificate file
            EVO_KEY_FILE: Path to client key file
            EVO_CONNECTION_POOL_MAXSIZE: Max connections in pool
            EVO_API_KEY: API key for authentication
            EVO_API_KEY_PREFIX: Prefix for API key

        Example:
            ```bash
            # Set environment variables
            export EVO_HOST="https://api.evo.com"
            export EVO_USERNAME="your_username"
            export EVO_PASSWORD="your_password"
            export EVO_TIMEOUT="60"
            export EVO_VERIFY_SSL="true"
            ```

            ```python
            # Load configuration
            from evo_client.config import EnvConfigLoader

            config = EnvConfigLoader.load_config()

            # Use with any client
            with SyncApiClient(config) as client:
                pass
            ```
        """
        mappings = env_mappings or cls.DEFAULT_ENV_MAPPINGS
        fallbacks = fallback_values or {}

        # Collect configuration values
        config_data = {}
        missing_required = []

        for config_key, env_key in mappings.items():
            full_env_key = f"{prefix}{env_key}"
            value = os.getenv(full_env_key)

            if value is not None:
                # Parse the value appropriately
                parsed_value = cls._parse_env_value(config_key, value)
                config_data[config_key] = parsed_value
            elif config_key in fallbacks:
                config_data[config_key] = fallbacks[config_key]
            elif required_vars and config_key in ["host", "username", "password"]:
                missing_required.append(full_env_key)

        # Check for required variables
        if missing_required:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_required)}\n"
                f"Please set these environment variables or use required_vars=False"
            )

        # Handle API key specially (it's a dict in Configuration)
        if "api_key" in config_data:
            api_key_value = config_data.pop("api_key")
            prefix_value = config_data.pop("api_key_prefix", "Bearer")
            config_data["api_key"] = {"ApiKey": api_key_value}
            config_data["api_key_prefix"] = {"ApiKey": prefix_value}

        # Create and return configuration
        try:
            return Configuration(**config_data)
        except Exception as e:
            raise ValueError(f"Invalid configuration from environment: {e}")

    @classmethod
    def _parse_env_value(cls, key: str, value: str) -> Any:
        """Parse environment variable value to appropriate type."""

        # Boolean values
        if key in ["verify_ssl", "assert_hostname"]:
            return value.lower() in ("true", "1", "yes", "on")

        # Numeric values
        if key == "timeout":
            try:
                return float(value)
            except ValueError:
                warn(f"Invalid timeout value '{value}', using default")
                return 60.0

        if key == "connection_pool_maxsize":
            try:
                return int(value)
            except ValueError:
                warn(f"Invalid connection_pool_maxsize value '{value}', using default")
                return 20

        # String values (default)
        return value

    @classmethod
    def check_env_vars(cls, prefix: str = "EVO_") -> Dict[str, Any]:
        """
        Check which environment variables are currently set.

        Args:
            prefix: Prefix for environment variables

        Returns:
            Dictionary of found environment variables

        Example:
            ```python
            # Check what's currently set
            found_vars = EnvConfigLoader.check_env_vars()
            print(f"Found variables: {list(found_vars.keys())}")
            ```
        """
        found = {}

        for config_key, env_key in cls.DEFAULT_ENV_MAPPINGS.items():
            full_env_key = f"{prefix}{env_key}"
            value = os.getenv(full_env_key)
            if value is not None:
                found[full_env_key] = value

        return found

    @classmethod
    def get_example_env_file(cls, prefix: str = "EVO_") -> str:
        """
        Generate example .env file content.

        Args:
            prefix: Prefix for environment variables

        Returns:
            Example .env file content as string

        Example:
            ```python
            # Generate example .env file
            env_content = EnvConfigLoader.get_example_env_file()

            # Save to file
            with open(".env.example", "w") as f:
                f.write(env_content)
            ```
        """
        examples = {
            "HOST": "https://evo-integracao-api.w12app.com.br",
            "USERNAME": "your_gym_dns",
            "PASSWORD": "your_secret_key",
            "TIMEOUT": "60",
            "VERIFY_SSL": "true",
            "PROXY": "# http://proxy.example.com:8080",
            "SSL_CA_CERT": "# /path/to/ca-cert.pem",
            "CERT_FILE": "# /path/to/client-cert.pem",
            "KEY_FILE": "# /path/to/client-key.pem",
            "CONNECTION_POOL_MAXSIZE": "20",
            "API_KEY": "# your_api_key_if_using_api_key_auth",
            "API_KEY_PREFIX": "# Bearer",
        }

        lines = [
            "# EVO Client Configuration",
            "# Copy to .env and fill in your values",
            "",
        ]

        for env_key, example_value in examples.items():
            full_key = f"{prefix}{env_key}"
            lines.append(f"{full_key}={example_value}")

        return "\n".join(lines)

    @classmethod
    def validate_required_vars(cls, prefix: str = "EVO_") -> bool:
        """
        Validate that required environment variables are set.

        Args:
            prefix: Prefix for environment variables

        Returns:
            True if all required variables are set

        Raises:
            ValueError: If required variables are missing

        Example:
            ```python
            # Check before creating config
            if EnvConfigLoader.validate_required_vars():
                config = EnvConfigLoader.load_config()
            ```
        """
        required = ["HOST", "USERNAME", "PASSWORD"]
        missing = []

        for env_key in required:
            full_key = f"{prefix}{env_key}"
            if not os.getenv(full_key):
                missing.append(full_key)

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        return True
