from typing import List, Optional, Dict
from datetime import datetime
import logging

from evo_client.api.prospects_api import ProspectsApi
from evo_client.core.api_client import ApiClient
from evo_client.models.prospects_resumo_api_view_model import (
    ProspectsResumoApiViewModel,
)
from evo_client.utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher

logger = logging.getLogger(__name__)


class ProspectsDataFetcher(BaseDataFetcher[ProspectsApi]):
    """Handles fetching and processing prospect-related data."""

    def __init__(
        self,
        prospects_api: ProspectsApi,
        branch_api_clients: Optional[Dict[str, ApiClient]] = None,
    ):
        """Initialize the prospects data fetcher.

        Args:
            prospects_api: The prospects API instance
            branch_api_clients: Optional dictionary mapping branch IDs to their API clients
        """
        super().__init__(prospects_api, branch_api_clients)

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
        default_client: bool = True,
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
            # Get prospects using paginated call with available branch IDs
            if default_client:
                result = paginated_api_call(
                    api_func=self.api.get_prospects,
                    unit_id="default",
                    id_prospect=id_prospect,
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
            else:
                result = []
                for branch_id in self.get_available_branch_ids():
                    branch_api = self.get_branch_api(branch_id, ProspectsApi)
                    if branch_api:
                        result.extend(
                            paginated_api_call(
                                api_func=branch_api.get_prospects,
                                unit_id=str(branch_id),
                                id_prospect=id_prospect,
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
