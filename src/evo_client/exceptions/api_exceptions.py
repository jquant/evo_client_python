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
    def __init__(self, message: Optional[str] = None, status: Optional[int] = None, reason: Optional[str] = None, http_resp: Optional[RESTResponse] = None):
        self.status = status
        self.reason = reason
        self.http_resp = http_resp
        
        if http_resp:
            self.status = http_resp.status
            self.reason = http_resp.reason
            message_parts = [
                f"({self.status})",
                f"Reason: {self.reason}",
                f"HTTP response headers: {http_resp.getheaders()}"
            ]
            if http_resp.data:
                message_parts.append(f"HTTP response body: {http_resp.data}")
            self.message = "\n".join(message_parts)
        elif status is not None and reason:
            if "SSLError" in reason:
                self.message = f"(0)\nReason: {reason}"
            else:
                self.message = f"({status})\nReason: {reason}"
        elif message:
            self.message = message
        else:
            self.message = "Unknown API error"
            
        super().__init__(self.message)
