from typing import List, Optional

from loguru import logger

from ...models.servicos_resumo_api_view_model import ServicosResumoApiViewModel
from ...sync.api.service_api import SyncServiceApi
from ...utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher


class ServiceDataFetcher(BaseDataFetcher):
    """Handles fetching and processing service-related data."""

    def fetch_services(
        self,
        id_service: Optional[int] = None,
        name: Optional[str] = None,
        active: Optional[bool] = None,
    ) -> List[ServicosResumoApiViewModel]:
        """Fetch services with various filters."""
        try:
            services = []
            for branch_id in self.get_available_branch_ids():
                branch_api = SyncServiceApi(api_client=self.get_branch_api(branch_id))
                if branch_api:
                    services.extend(
                        paginated_api_call(
                            api_func=branch_api.get_services,
                            branch_id=str(branch_id),
                            service_id=id_service,
                            name=name,
                            active=active,
                        )
                    )

            return services or []

        except Exception as e:
            logger.error(f"Error fetching services: {str(e)}")
            raise ValueError(f"Error fetching services: {str(e)}")
