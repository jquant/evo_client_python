from datetime import datetime
from typing import List, Optional

from loguru import logger

from ...models.entradas_resumo_api_view_model import EntradasResumoApiViewModel
from ...models.gym_model import GymEntry
from ...sync.api.entries_api import SyncEntriesApi
from ...utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher


class EntriesDataFetcher(BaseDataFetcher):
    """Handles fetching and processing entry-related data."""

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
            entries: List[EntradasResumoApiViewModel] = []
            # Get entries from branch clients
            for branch_id in self.get_available_branch_ids():
                branch_api = SyncEntriesApi(api_client=self.get_branch_api(branch_id))
                if branch_api:
                    try:
                        branch_result = paginated_api_call(
                            api_func=branch_api.get_entries,
                            branch_id_logging=str(branch_id),
                            register_date_start=register_date_start,
                            register_date_end=register_date_end,
                            entry_id=id_entry,
                            member_id=id_member,
                        )
                        if branch_result:
                            entries.extend(branch_result)
                    except Exception as e:
                        logger.warning(
                            f"Failed to fetch entries for branch {branch_id}: {e}"
                        )

            return [GymEntry.model_validate(entry) for entry in entries]

        except Exception as e:
            logger.error(f"Error fetching entries: {str(e)}")
            raise ValueError(f"Error fetching entries: {str(e)}")
