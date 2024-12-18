from typing import List, Optional, Dict
from datetime import datetime
import logging

from evo_client.api.entries_api import EntriesApi
from evo_client.models.gym_model import GymEntry
from evo_client.core.api_client import ApiClient
from evo_client.utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher

logger = logging.getLogger(__name__)


class EntriesDataFetcher(BaseDataFetcher[EntriesApi]):
    """Handles fetching and processing entry-related data."""

    def __init__(
        self,
        entries_api: EntriesApi,
        branch_api_clients: Optional[Dict[str, ApiClient]] = None,
    ):
        """Initialize the entries data fetcher.

        Args:
            entries_api: The entries API instance
            branch_api_clients: Optional dictionary mapping branch IDs to their API clients
        """
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
        try:
            entries = []

            # Get entries from default client
            result = paginated_api_call(
                api_func=self.api.get_entries,
                register_date_start=register_date_start,
                register_date_end=register_date_end,
                id_entry=id_entry,
                id_member=id_member,
            )
            if result:
                entries.extend(result)

            # Get entries from branch clients
            for branch_id in self.get_available_branch_ids():
                branch_api = self.get_branch_api(branch_id, EntriesApi)
                if branch_api:
                    try:
                        branch_result = paginated_api_call(
                            api_func=branch_api.get_entries,
                            register_date_start=register_date_start,
                            register_date_end=register_date_end,
                            id_entry=id_entry,
                            id_member=id_member,
                        )
                        if branch_result:
                            entries.extend(branch_result)
                    except Exception as e:
                        logger.warning(
                            f"Failed to fetch entries for branch {branch_id}: {e}"
                        )

            return entries

        except Exception as e:
            logger.error(f"Error fetching entries: {str(e)}")
            raise
