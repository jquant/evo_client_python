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
    """Base exception for API errors."""

    def __init__(
        self,
        status: Optional[int] = None,
        reason: Optional[str] = None,
        http_resp: Optional[RESTResponse] = None,
    ):
        self.status = http_resp.status if http_resp else status
        self.reason = http_resp.reason if http_resp else reason
        self.body = http_resp.data if http_resp else None
        self.headers = http_resp.getheaders() if http_resp else None

    def __str__(self) -> str:
        """Format error message."""
        parts = [f"({self.status})", f"Reason: {self.reason}"]

        if self.headers:
            parts.append(f"HTTP response headers: {self.headers}")
        if self.body:
            parts.append(f"HTTP response body: {self.body}")

        return "\n".join(parts)
