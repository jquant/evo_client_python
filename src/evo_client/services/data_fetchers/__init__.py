"""Data fetchers for retrieving data from various API endpoints."""

import abc
from typing import Dict, Optional, List
from evo_client.core.api_client import ApiClient


class BranchApiClientManager:
    """Manager for branch API clients."""

    def __init__(self, branch_api_clients: Dict[str, ApiClient]):
        """Initialize the data fetcher.

        Args:
            branch_api_clients: Optional dictionary mapping branch IDs to their API clients.
                              Only the provided branch clients will be used for fetching data.
        """
        self.branch_api_clients = branch_api_clients or {}
        # Store branch IDs as integers for easier access
        self.branch_ids = (
            [int(bid) for bid in self.branch_api_clients.keys()]
            if branch_api_clients
            else []
        )


class BaseDataFetcher(abc.ABC):
    """Base class for all data fetchers."""

    def __init__(self, client_manager: BranchApiClientManager):
        """Initialize the data fetcher.

        Args:
            client_manager: The client manager instance
        """
        self.client_manager = client_manager

    def get_branch_api(self, branch_id: int) -> Optional[ApiClient]:
        """Get a branch-specific API instance.

        Args:
            branch_id: The branch ID

        Returns:
            Branch-specific API instance or None if not found
        """
        branch_client = self.client_manager.branch_api_clients.get(str(branch_id))
        return branch_client

    def get_available_branch_ids(self) -> List[int]:
        """Get list of branch IDs for which we have API clients.

        Returns:
            List of branch IDs
        """
        return self.client_manager.branch_ids


__all__ = [
    "BaseDataFetcher",
]
