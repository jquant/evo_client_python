"""Base class for all sync API implementations."""

from typing import Optional

from ..core.api_client import SyncApiClient


class SyncBaseApi:
    """Base class for all synchronous API classes."""

    def __init__(self, api_client: Optional[SyncApiClient] = None):
        """
        Initialize the sync API.

        Args:
            api_client: Optional sync API client. If not provided, creates a new one.
        """
        self.api_client = api_client or SyncApiClient()

    def __enter__(self):
        """Context manager entry."""
        if hasattr(self.api_client, "__enter__"):
            self.api_client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if hasattr(self.api_client, "__exit__"):
            self.api_client.__exit__(exc_type, exc_val, exc_tb)
