from typing import Optional

from ..core.response import RESTResponse


class ApiClientError(Exception):
    """Base exception for API client errors."""


class RequestError(ApiClientError):
    """Raised when a request fails."""


class DeserializationError(ApiClientError):
    """Raised when deserialization fails."""


class ConfigurationError(ApiClientError):
    """Raised when configuration is invalid."""


class ApiException(Exception):
    """
    Generic API Exception
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
