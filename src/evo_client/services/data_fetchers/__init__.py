"""Data fetchers for retrieving data from various API endpoints."""

from typing import Dict, Optional, List, Type, TypeVar, Generic
from evo_client.core.api_client import ApiClient
from evo_client.api.base import BaseApi

T = TypeVar("T")
ClassType = TypeVar("ClassType", bound=BaseApi)


class BaseDataFetcher(Generic[T]):
    """Base class for all data fetchers."""

    def __init__(
        self, api: T, branch_api_clients: Optional[Dict[str, ApiClient]] = None
    ):
        """Initialize the data fetcher.

        Args:
            api: The default API instance
            branch_api_clients: Optional dictionary mapping branch IDs to their API clients.
                              Only the provided branch clients will be used for fetching data.
        """
        self.api = api
        self.branch_api_clients = branch_api_clients or {}
        # Store branch IDs as integers for easier access
        self.branch_ids = (
            [int(bid) for bid in self.branch_api_clients.keys()]
            if branch_api_clients
            else []
        )

    def get_branch_api(
        self, branch_id: int, api_class: Type[ClassType]
    ) -> Optional[ClassType]:
        """Get a branch-specific API instance.

        Args:
            branch_id: The branch ID
            api_class: The API class to instantiate

        Returns:
            Branch-specific API instance or None if not found
        """
        branch_client = self.branch_api_clients.get(str(branch_id))
        if branch_client:
            return api_class(api_client=branch_client)
        return None

    def get_available_branch_ids(self) -> List[int]:
        """Get list of branch IDs for which we have API clients.

        Returns:
            List of branch IDs
        """
        return self.branch_ids


__all__ = [
    "BaseDataFetcher",
]
