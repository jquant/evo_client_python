"""Clean asynchronous Service API."""

from typing import List, Optional, cast

from ...models.servicos_resumo_api_view_model import ServicosResumoApiViewModel
from .base import AsyncBaseApi


class AsyncServiceApi(AsyncBaseApi):
    """Clean asynchronous Service API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/service"

    async def get_services(
        self,
        service_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        active: Optional[bool] = None,
    ) -> List[ServicosResumoApiViewModel]:
        """
        Get services list with optional filtering.

        Args:
            service_id: Filter by Service Id
            name: Filter by service name
            branch_id: Filter by service branch ID (Only for multilocation key)
            take: Total number of records to return (Maximum of 50)
            skip: Total number of records to skip
            active: Filter by active/inactive services

        Returns:
            List of services containing details like:
            - Service ID, name, and description
            - Pricing information
            - Availability and scheduling
            - Branch assignments
            - Status and settings

        Example:
            >>> async with AsyncServiceApi() as api:
            ...     services = await api.get_services(
            ...         name="Personal Training",
            ...         active=True,
            ...         take=10
            ...     )
            ...     for service in services:
            ...         print(f"Service: {service.name}")
            ...         print(f"Price: {service.price}")
            ...         print(f"Branch: {service.branch_name}")
        """
        params = {
            "idService": service_id,
            "name": name,
            "idBranch": branch_id,
            "take": take,
            "skip": skip,
            "active": active,
        }

        result = await self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[ServicosResumoApiViewModel],
            auth_settings=["Basic"],
        )
        return cast(List[ServicosResumoApiViewModel], result)
