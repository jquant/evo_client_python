from typing import List, Optional, Dict
from datetime import datetime

from evo_client.api.entries_api import EntriesApi
from evo_client.models.gym_model import GymEntry
from evo_client.core.api_client import ApiClient
from evo_client.utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher


class EntriesDataFetcher(BaseDataFetcher):
    """Handles fetching and processing entry-related data."""
    
    def __init__(self, entries_api: EntriesApi, branch_api_clients: Optional[Dict[str, ApiClient]] = None):
        super().__init__(entries_api, branch_api_clients)
    
    def fetch_entries(
        self,
        register_date_start: Optional[datetime] = None,
        register_date_end: Optional[datetime] = None,
        id_entry: Optional[int] = None,
        id_member: Optional[int] = None,
    ) -> List[GymEntry]:
        """Fetch entries with various filters.

        Args:
            register_date_start: Filter by registration start date (YYYY-MM-DDTHH:mm:ssZ)
            register_date_end: Filter by registration end date (YYYY-MM-DDTHH:mm:ssZ)
            id_entry: Filter by entry ID
            id_member: Filter by member ID

        Returns:
            List[GymEntry]: List of entries matching the filters
        """
        return paginated_api_call(
            api_func=self.api.get_entries,
            parallel_units=self.branch_ids,
            register_date_start=register_date_start,
            register_date_end=register_date_end,
            id_entry=id_entry,
            id_member=id_member
        ) 