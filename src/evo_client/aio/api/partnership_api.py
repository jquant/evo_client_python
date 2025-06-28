"""Clean asynchronous Partnership API."""

from datetime import datetime
from typing import List, Optional, cast

from ...models.convenios_api_view_model import ConveniosApiViewModel
from .base import AsyncBaseApi


class AsyncPartnershipApi(AsyncBaseApi):
    """Clean asynchronous Partnership API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/partnership"

    async def get_partnerships(
        self,
        status: Optional[int] = None,
        description: Optional[str] = None,
        dt_created: Optional[datetime] = None,
    ) -> List[ConveniosApiViewModel]:
        """
        Get partnerships with optional filtering.

        Args:
            status: Filter by status: 0=Both, 1=Active, 2=Inactive
            description: Filter by partnership name
            dt_created: Filter by registration date

        Returns:
            List of partnerships including:
            - Partnership IDs and names
            - Status information (active/inactive)
            - Registration dates and details
            - Terms and conditions
            - Contact information

        Example:
            >>> async with AsyncPartnershipApi() as api:
            ...     partnerships = await api.get_partnerships(
            ...         status=1,  # Active only
            ...         description="Health"
            ...     )
            ...     for partnership in partnerships:
            ...         print(f"Partnership: {partnership.name}")
            ...         print(f"Status: {'Active' if partnership.status else 'Inactive'}")
        """
        params = {
            "status": status,
            "description": description,
            "dtCreated": dt_created,
        }

        result = await self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[ConveniosApiViewModel],
            auth_settings=["Basic"],
        )
        return cast(List[ConveniosApiViewModel], result)
