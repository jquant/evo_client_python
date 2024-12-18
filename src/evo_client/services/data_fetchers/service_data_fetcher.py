from typing import List, Optional, Dict

from ...api.service_api import ServiceApi
from ...core.api_client import ApiClient
from ...models.servicos_resumo_api_view_model import ServicosResumoApiViewModel
from ...utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher
from loguru import logger


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
        default_client: bool = True,
    ) -> List[ServicosResumoApiViewModel]:
        """Fetch services with various filters."""
        try:
            if default_client:
                services = paginated_api_call(
                    api_func=self.api.get_services,
                    unit_id="default",
                    service_id=id_service,
                    name=name,
                    active=active,
                )
            else:
                services = []
                for branch_id in self.get_available_branch_ids():
                    branch_api = self.get_branch_api(branch_id, ServiceApi)
                    if branch_api:
                        services.extend(
                            paginated_api_call(
                                api_func=branch_api.get_services,
                                unit_id=str(branch_id),
                                service_id=id_service,
                                name=name,
                                active=active,
                            )
                        )

            return services or []

        except Exception as e:
            logger.error(f"Error fetching services: {str(e)}")
            raise ValueError(f"Error fetching services: {str(e)}")
