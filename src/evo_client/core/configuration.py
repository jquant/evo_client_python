"""Configuration module for EVO API client.

Handles authentication, logging, and connection settings for API requests.
"""

from __future__ import annotations

import logging
import multiprocessing
import sys
from typing import Callable, Dict, Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, ValidationInfo, field_validator
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)


class Configuration(BaseModel):
    """Configuration settings for the API client."""

    # Base settings with validation
    host: str = Field(
        default="https://evo-integracao-api.w12app.com.br", validate_default=True
    )
    base_path: str = Field(default="/api/v1")
    default_headers: Dict[str, str] = Field(default_factory=dict)
    temp_folder_path: Optional[str] = None
    timeout: float = Field(default=60.0, validate_default=True)

    # Authentication
    api_key: Dict[str, str] = Field(default_factory=dict)
    api_key_prefix: Dict[str, str] = Field(default_factory=dict)
    refresh_api_key_hook: Optional[Callable[["Configuration"], None]] = None
    username: str = ""
    password: str = ""

    # SSL/TLS
    verify_ssl: bool = True
    ssl_ca_cert: Optional[str] = None
    cert_file: Optional[str] = Field(default=None, validate_default=True)
    key_file: Optional[str] = Field(default=None, validate_default=True)
    assert_hostname: Optional[bool] = None

    # Connection
    connection_pool_maxsize: int = Field(
        default_factory=lambda: multiprocessing.cpu_count() * 5
    )
    proxy: Optional[str] = None
    safe_chars_for_path_param: str = ""

    @field_validator("host")
    @classmethod
    def validate_host_format(cls, v: str) -> str:
        """Validate host URL format."""
        try:
            parsed = urlparse(v)
            if not all([parsed.scheme, parsed.netloc]):
                raise ValueError("Invalid host URL format")
        except Exception as e:
            raise ValueError(f"Invalid host URL format: {e}")
        return v

    @field_validator("timeout")
    @classmethod
    def validate_timeout_positive(cls, v: float) -> float:
        """Validate timeout is positive."""
        if v <= 0:
            raise ValueError("Timeout must be positive")
        return v

    @field_validator("cert_file", "key_file")
    @classmethod
    def validate_cert_key_files(
        cls, v: Optional[str], info: ValidationInfo
    ) -> Optional[str]:
        """Validate cert_file and key_file are provided together."""
        field_name = info.field_name
        other_field = "key_file" if field_name == "cert_file" else "cert_file"

        # If we're setting a value
        if other_field in info.data:
            if v is not None:
                # Check if the other field has a value
                if info.data[other_field] is None:
                    raise ValueError(
                        f"{other_field} is required when {field_name} is provided"
                    )
            else:
                if info.data[other_field] is not None:
                    raise ValueError(
                        f"{field_name} is required when {other_field} is provided"
                    )

        return v

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

    def get_basic_auth_token(self) -> Optional[HTTPBasicAuth]:
        """Get HTTP basic authentication header."""
        if self.username or self.password:
            credentials = HTTPBasicAuth(self.username, self.password)
            return credentials
        return None

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
