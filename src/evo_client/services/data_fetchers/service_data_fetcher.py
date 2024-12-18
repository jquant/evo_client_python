from typing import List, Optional, Dict

from evo_client.api.service_api import ServiceApi
from evo_client.core.api_client import ApiClient
from evo_client.models.servicos_resumo_api_view_model import ServicosResumoApiViewModel
from evo_client.utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher


class ServiceDataFetcher(BaseDataFetcher):
    """Handles fetching and processing service-related data."""
    
    def __init__(self, service_api: ServiceApi, branch_api_clients: Optional[Dict[str, ApiClient]] = None):
        super().__init__(service_api, branch_api_clients)
    
    def fetch_services(
        self,
        id_service: Optional[int] = None,
        name: Optional[str] = None,
        active: Optional[bool] = None,
    ) -> List[ServicosResumoApiViewModel]:
        """Fetch services with various filters."""
        return paginated_api_call(
            api_func=self.api.get_services,
            parallel_units=self.branch_ids,
            id_service=id_service,
            name=name,
            active=active,
        )
