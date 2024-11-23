"""Configuration module for EVO API client.

Handles authentication, logging, and connection settings for API requests.
"""

from __future__ import annotations
import copy
import logging
import multiprocessing
import sys
import urllib3
from dataclasses import dataclass, field
from typing import Dict, Optional, Callable, ClassVar
from urllib.parse import urlparse
from pydantic import BaseModel
from base64 import b64encode

logger = logging.getLogger(__name__)


class Configuration(BaseModel):
    """Configuration settings for the API client."""

    # Base settings with validation
    host: str = field(default="https://evo-integracao-api.w12app.com.br")
    temp_folder_path: Optional[str] = None
    timeout: float = field(default=60.0, metadata={"min_value": 0.1})

    # Authentication
    api_key: Dict[str, str] = field(default_factory=dict)
    api_key_prefix: Dict[str, str] = field(default_factory=dict)
    refresh_api_key_hook: Optional[Callable[["Configuration"], None]] = None
    username: str = ""
    password: str = ""

    # Logging
    logger_format: str = "%(asctime)s %(levelname)s %(message)s"
    logger_file: Optional[str] = None
    debug: bool = False

    # SSL/TLS
    verify_ssl: bool = True
    ssl_ca_cert: Optional[str] = None
    cert_file: Optional[str] = None
    key_file: Optional[str] = None
    assert_hostname: Optional[bool] = None

    # Connection
    connection_pool_maxsize: int = field(
        default_factory=lambda: multiprocessing.cpu_count() * 5
    )
    proxy: Optional[str] = None
    safe_chars_for_path_param: str = ""

    def __call__(self) -> Configuration:
        if self._default_instance is None:
            self._default_instance = self
        assert self._default_instance is not None
        return copy.copy(self._default_instance)

    def set_default(self, default: Configuration) -> None:
        """Set default configuration instance."""
        self._default_instance = copy.copy(default)

    def __post_init__(self):
        """Initialize logging configuration and validate settings."""
        self._validate_settings()
        self._setup_logging()

    def _validate_settings(self) -> None:
        """Validate configuration settings."""
        # Validate host URL
        try:
            parsed = urlparse(self.host)
            if not all([parsed.scheme, parsed.netloc]):
                raise ValueError("Invalid host URL format")
        except Exception as e:
            raise ValueError(f"Invalid host URL: {e}")

        # Validate timeout
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")

        # Validate SSL settings
        if self.cert_file and not self.key_file:
            raise ValueError("key_file is required when cert_file is provided")

    def _setup_logging(self) -> None:
        """Configure logging handlers and formatters."""
        self.logger_formatter = logging.Formatter(self.logger_format)
        self._configure_logger_handlers()
        self._set_debug_level()

    def _configure_logger_handlers(self) -> None:
        """Set up file or stream handlers based on configuration."""
        if self.logger_file:
            handler = logging.FileHandler(self.logger_file)
        else:
            handler = logging.StreamHandler()

        handler.setFormatter(self.logger_formatter)
        logger.addHandler(handler)

    def _set_debug_level(self) -> None:
        """Set logging level based on debug setting."""
        logger.setLevel(logging.DEBUG if self.debug else logging.WARNING)

    def get_api_key_with_prefix(self, identifier: str) -> Optional[str]:
        """Get API key with optional prefix."""
        if self.refresh_api_key_hook:
            try:
                self.refresh_api_key_hook(self)
            except Exception as e:
                logger.error(f"Error refreshing API key: {e}")

        if key := self.api_key.get(identifier):
            if prefix := self.api_key_prefix.get(identifier):
                return f"{prefix} {key}"
            return key
        return None

    def get_basic_auth_token(self) -> str:
        """Get HTTP basic authentication header."""
        if self.username or self.password:
            credentials = f"{self.username}:{self.password}"
            encoded_credentials = b64encode(credentials.encode("utf-8")).decode("utf-8")
            return encoded_credentials
        return ""

    def auth_settings(self) -> Dict[str, Dict]:
        """Get authentication settings dictionary."""
        auth_settings = {
            "Basic": {
                "type": "basic",
                "in": "header",
                "key": "Authorization",
                "value": self.get_basic_auth_token(),
            }
        }

        # Add API key auth if configured
        if self.api_key:
            api_key_value = self.get_api_key_with_prefix("ApiKey")
            if api_key_value is not None:  # Only add if we have a valid key
                auth_settings["ApiKey"] = {
                    "type": "api_key",
                    "in": "header",
                    "key": "X-API-Key",
                    "value": api_key_value,
                }

        return auth_settings

    def to_debug_report(self) -> str:
        """Generate debug report with system information."""
        return (
            "Python SDK Debug Report:\n"
            f"OS: {sys.platform}\n"
            f"Python Version: {sys.version}\n"
            "Version of the API: v1\n"
            "SDK Package Version: 1.0.0"
        )
