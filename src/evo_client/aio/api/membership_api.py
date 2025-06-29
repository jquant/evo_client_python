"""Clean asynchronous Membership API."""

from typing import List, Literal, Optional, Union, cast

from ...models.contratos_resumo_api_view_model import (
    ContratosResumoApiViewModel,
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

    async def get_memberships_v1(
        self,
        membership_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        active: Optional[bool] = None,
    ) -> List[ContratosResumoApiViewModel]:
        """
        Get memberships using v1 API (returns list).

        Args:
            membership_id: Filter by membership ID
            name: Filter by membership name
            branch_id: Filter by branch ID (only for multilocation keys)
            take: Number of records to return (max 50)
            skip: Number of records to skip
            active: Filter by active/inactive status

        Returns:
            List of membership contracts

        Example:
            >>> async with AsyncMembershipApi() as api:
            ...     memberships = await api.get_memberships_v1(
            ...         name="Premium",
            ...         active=True,
            ...         take=10
            ...     )
            ...     for membership in memberships:
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
            resource_path=self.base_path_v1,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[ContratosResumoApiViewModel],
            auth_settings=["Basic"],
        )
        return cast(List[ContratosResumoApiViewModel], result)

    async def get_memberships_v2(
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

    async def get_memberships(
        self,
        membership_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        active: Optional[bool] = None,
        version: Literal["v1", "v2"] = "v2",
    ) -> Union[List[ContratosResumoApiViewModel], ContratosResumoContainerViewModel]:
        """
        Get memberships with version selection (convenience method).

        Args:
            membership_id: Filter by membership ID
            name: Filter by membership name
            branch_id: Filter by branch ID (only for multilocation keys)
            take: Number of records to return (max 50)
            skip: Number of records to skip
            active: Filter by active/inactive status
            version: API version to use ("v1" or "v2")

        Returns:
            List (v1) or Container (v2) depending on version

        Example:
            >>> async with AsyncMembershipApi() as api:
            ...     # Get v2 container (default)
            ...     container = await api.get_memberships(name="Premium")
            ...
            ...     # Get v1 list
            ...     memberships = await api.get_memberships(name="Premium", version="v1")
        """
        if version == "v1":
            return await self.get_memberships_v1(
                membership_id=membership_id,
                name=name,
                branch_id=branch_id,
                take=take,
                skip=skip,
                active=active,
            )
        else:
            return await self.get_memberships_v2(
                membership_id=membership_id,
                name=name,
                branch_id=branch_id,
                take=take,
                skip=skip,
                active=active,
            )

    async def list_memberships(
        self,
        membership_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        active: Optional[bool] = None,
        version: Literal["v1", "v2"] = "v2",
    ) -> List[ContratosResumoApiViewModel]:
        """
        List all memberships (always returns a list).

        Args:
            membership_id: Filter by membership ID
            name: Filter by membership name
            branch_id: Filter by branch ID (only for multilocation keys)
            take: Number of records to return (max 50)
            skip: Number of records to skip
            active: Filter by active/inactive status
            version: API version to use ("v1" or "v2")

        Returns:
            List of memberships

        Raises:
            ValueError: If response format is invalid

        Example:
            >>> async with AsyncMembershipApi() as api:
            ...     memberships = await api.list_memberships(
            ...         active=True,
            ...         take=20
            ...     )
            ...     for membership in memberships:
            ...         print(f"{membership.name} - Active: {membership.active}")
        """
        response = await self.get_memberships(
            membership_id=membership_id,
            name=name,
            branch_id=branch_id,
            take=take,
            skip=skip,
            active=active,
            version=version,
        )

        if isinstance(response, list):
            return response
        elif isinstance(response, ContratosResumoContainerViewModel) and response.list:
            return response.list
        else:
            raise ValueError(
                f"Invalid response type: 'list' is missing from the response. Response: {response}"
            )
