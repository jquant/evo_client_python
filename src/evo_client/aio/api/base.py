"""Base class for all async API implementations."""

from typing import Optional

from ..core.api_client import AsyncApiClient


class AsyncBaseApi:
    """Base class for all async API classes."""

    def __init__(self, api_client: Optional[AsyncApiClient] = None):
        """
        Initialize the async API.

        Args:
            api_client: Optional async API client. If not provided, creates a new one.
        """
        self.api_client = api_client or AsyncApiClient()

    async def __aenter__(self):
        """Async context manager entry."""
        if hasattr(self.api_client, "__aenter__"):
            await self.api_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if hasattr(self.api_client, "__aexit__"):
            await self.api_client.__aexit__(exc_type, exc_val, exc_tb)
