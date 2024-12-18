from typing import List, Optional, Dict

from evo_client.api.service_api import ServiceApi
from evo_client.core.api_client import ApiClient
from evo_client.models.servicos_resumo_api_view_model import ServicosResumoApiViewModel
from evo_client.utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher
import logging

logger = logging.getLogger(__name__)


class ServiceDataFetcher(BaseDataFetcher[ServiceApi]):
    """Handles fetching and processing service-related data."""

    def __init__(
        self,
        service_api: ServiceApi,
        branch_api_clients: Optional[Dict[str, ApiClient]] = None,
    ):
        """Initialize the service data fetcher.

        Args:
            service_api: The service API instance
            branch_api_clients: Optional dictionary mapping branch IDs to their API clients
        """
        super().__init__(service_api, branch_api_clients)

    def fetch_services(
        self,
        id_service: Optional[int] = None,
        name: Optional[str] = None,
        active: Optional[bool] = None,
    ) -> List[ServicosResumoApiViewModel]:
        """Fetch services with various filters."""
        try:
            result = paginated_api_call(
                api_func=self.api.get_services,
                parallel_units=self.get_available_branch_ids(),
                service_id=id_service,
                name=name,
                active=active,
            )

            return result or []

        except Exception as e:
            logger.error(f"Error fetching services: {str(e)}")
            raise
