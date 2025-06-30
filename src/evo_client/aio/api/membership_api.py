"""Clean asynchronous Membership API."""

from typing import List, Optional, cast

from ...models.contratos_resumo_api_view_model import (
    ContratosResumoContainerViewModel,
)
from ...models.w12_utils_category_membership_view_model import (
    W12UtilsCategoryMembershipViewModel,
)
from .base import AsyncBaseApi


class AsyncMembershipApi(AsyncBaseApi):
    """Clean asynchronous Membership API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path_v1 = "/api/v1/membership"
        self.base_path_v2 = "/api/v2/membership"

    async def get_categories(self) -> List[W12UtilsCategoryMembershipViewModel]:
        """
        Get membership categories.

        Returns:
            List of membership categories

        Example:
            >>> async with AsyncMembershipApi() as api:
            ...     categories = await api.get_categories()
            ...     for category in categories:
            ...         print(f"{category.name} - {category.description}")
        """
        result = await self.api_client.call_api(
            resource_path=f"{self.base_path_v1}/category",
            method="GET",
            response_type=List[W12UtilsCategoryMembershipViewModel],
            auth_settings=["Basic"],
        )
        return cast(List[W12UtilsCategoryMembershipViewModel], result)

    async def get_memberships(
        self,
        membership_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        active: Optional[bool] = None,
    ) -> ContratosResumoContainerViewModel:
        """
        Get memberships using v2 API (returns container with metadata).

        Args:
            membership_id: Filter by membership ID
            name: Filter by membership name
            branch_id: Filter by branch ID (only for multilocation keys)
            take: Number of records to return (max 50)
            skip: Number of records to skip
            active: Filter by active/inactive status

        Returns:
            Container with membership list and metadata

        Example:
            >>> async with AsyncMembershipApi() as api:
            ...     container = await api.get_memberships_v2(
            ...         name="Premium",
            ...         active=True,
            ...         take=10
            ...     )
            ...     print(f"Total: {container.total}")
            ...     for membership in container.list:
            ...         print(f"{membership.name} - {membership.price}")
        """
        params = {
            "idMembership": membership_id,
            "name": name,
            "idBranch": branch_id,
            "take": take,
            "skip": skip,
            "active": active,
        }

        result = await self.api_client.call_api(
            resource_path=self.base_path_v2,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=ContratosResumoContainerViewModel,
            auth_settings=["Basic"],
        )
        return cast(ContratosResumoContainerViewModel, result)
