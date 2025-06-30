from datetime import datetime
from typing import List, Optional

from loguru import logger

from ...models.prospects_resumo_api_view_model import ProspectsResumoApiViewModel
from ...sync.api.prospects_api import SyncProspectsApi
from ...utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher


class ProspectsDataFetcher(BaseDataFetcher):
    """Handles fetching and processing prospect-related data."""

    def fetch_prospects(
        self,
        id_prospect: Optional[int] = None,
        name: Optional[str] = None,
        document: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        register_date_start: Optional[datetime] = None,
        register_date_end: Optional[datetime] = None,
        conversion_date_start: Optional[datetime] = None,
        conversion_date_end: Optional[datetime] = None,
        gympass_id: Optional[str] = None,
    ) -> List[ProspectsResumoApiViewModel]:
        """Fetch prospects with various filters.

        Args:
            id_prospect: Filter by prospect ID
            name: Filter by prospect name
            document: Filter by document number
            email: Filter by email address
            phone: Filter by phone number
            register_date_start: Filter by registration start date
            register_date_end: Filter by registration end date
            conversion_date_start: Filter by conversion start date
            conversion_date_end: Filter by conversion end date
            gympass_id: Filter by Gympass ID

        Returns:
            List[ProspectsResumoApiViewModel]: List of prospects matching the filters
        """
        try:
            result = []
            for branch_id in self.get_available_branch_ids():
                branch_api = SyncProspectsApi(api_client=self.get_branch_api(branch_id))
                if branch_api:
                    result.extend(
                        paginated_api_call(
                            api_func=branch_api.get_prospects,
                            branch_id_logging=str(branch_id),
                            prospect_id=id_prospect,
                            name=name,
                            document=document,
                            email=email,
                            phone=phone,
                            register_date_start=register_date_start,
                            register_date_end=register_date_end,
                            conversion_date_start=conversion_date_start,
                            conversion_date_end=conversion_date_end,
                            gympass_id=gympass_id,
                        )
                    )

            return result or []

        except Exception as e:
            logger.error(f"Error fetching prospects: {str(e)}")
            raise ValueError(f"Error fetching prospects: {str(e)}")
