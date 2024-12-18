from typing import List, Optional, Dict
from datetime import datetime

from evo_client.api.prospects_api import ProspectsApi
from evo_client.core.api_client import ApiClient
from evo_client.models.prospects_resumo_api_view_model import ProspectsResumoApiViewModel
from evo_client.utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher


class ProspectsDataFetcher(BaseDataFetcher):
    """Handles fetching and processing prospect-related data."""
    
    def __init__(self, prospects_api: ProspectsApi, branch_api_clients: Optional[Dict[str, ApiClient]] = None):
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
    ) -> List[ProspectsResumoApiViewModel]:
        """Fetch prospects with various filters."""
        return paginated_api_call(
            api_func=self.api.get_prospects,
            parallel_units=self.branch_ids,
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
