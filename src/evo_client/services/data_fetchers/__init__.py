"""Data fetchers for retrieving data from various API endpoints."""

from typing import Dict, Optional, Any
from evo_client.core.api_client import ApiClient

class BaseDataFetcher:
    """Base class for all data fetchers."""
    def __init__(self, api: Any, branch_api_clients: Optional[Dict[str, ApiClient]] = None):
        self.api = api
        self.branch_api_clients = branch_api_clients or {}
        self.branch_ids = [int(bid) for bid in self.branch_api_clients.keys()] if branch_api_clients else []

__all__ = [
    'BaseDataFetcher',
] 