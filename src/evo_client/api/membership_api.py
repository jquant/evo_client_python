from multiprocessing.pool import AsyncResult
from typing import Any, List, Literal, Optional, Union, overload

from loguru import logger

from ..core.api_client import ApiClient
from ..models.contratos_resumo_api_view_model import (
    ContratosResumoApiViewModel,
    ContratosResumoContainerViewModel,
)
from ..models.w12_utils_category_membership_view_model import (
    W12UtilsCategoryMembershipViewModel,
)
from .base import BaseApi


class MembershipApi(BaseApi):
    """Membership API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        super().__init__(api_client)
        self.base_path_v1 = "/api/v1/membership"
        self.base_path_v2 = "/api/v2/membership"

    @overload
    def get_categories(
        self, async_req: Literal[False] = False
    ) -> List[W12UtilsCategoryMembershipViewModel]:
        ...

    @overload
    def get_categories(self, async_req: Literal[True] = True) -> AsyncResult[Any]:
        ...

    def get_categories(
        self, async_req: bool = False
    ) -> Union[List[W12UtilsCategoryMembershipViewModel], AsyncResult[Any]]:
        """Get membership categories."""
        return self.api_client.call_api(
            resource_path=f"{self.base_path_v1}/category",
            method="GET",
            response_type=List[W12UtilsCategoryMembershipViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def get_memberships(
        self,
        membership_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        active: Optional[bool] = None,
        version: Literal["v1"] = "v1",
        async_req: Literal[False] = False,
    ) -> List[ContratosResumoApiViewModel]:
        ...

    @overload
    def get_memberships(
        self,
        membership_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        active: Optional[bool] = None,
        version: Literal["v2"] = "v2",
        async_req: Literal[False] = False,
    ) -> ContratosResumoContainerViewModel:
        ...

    @overload
    def get_memberships(
        self,
        membership_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        active: Optional[bool] = None,
        version: Literal["v1", "v2"] = "v2",
        async_req: Literal[False] = False,
    ) -> Union[List[ContratosResumoApiViewModel], ContratosResumoContainerViewModel]:
        ...

    @overload
    def get_memberships(
        self,
        membership_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        active: Optional[bool] = None,
        version: Literal["v1", "v2"] = "v2",
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]:
        ...

    def get_memberships(
        self,
        membership_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        active: Optional[bool] = None,
        version: Literal["v1", "v2"] = "v2",
        async_req: bool = False,
    ) -> Union[
        ContratosResumoContainerViewModel,
        List[ContratosResumoApiViewModel],
        AsyncResult[Any],
    ]:
        """
        Get memberships list with optional filtering.

        Args:
            membership_id: Filter by membership ID
            name: Filter by membership name
            branch_id: Filter by branch ID (only for multilocation keys)
            take: Number of records to return (max 50)
            skip: Number of records to skip
            active: Filter by active/inactive status
            async_req: Execute request asynchronously
        """
        params = {
            "idMembership": membership_id,
            "name": name,
            "idBranch": branch_id,
            "take": take,
            "skip": skip,
            "active": active,
        }
        if version == "v1":
            resource_path = self.base_path_v1
            response_type = List[ContratosResumoApiViewModel]
        else:
            resource_path = self.base_path_v2
            response_type = ContratosResumoContainerViewModel

        # Use the container model as the response type
        response = self.api_client.call_api(
            resource_path=resource_path,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=response_type,
            auth_settings=["Basic"],
            async_req=async_req,
        )

        # For async requests, return the AsyncResult directly
        if async_req:
            return response

        # For synchronous requests, extract the list from the container
        return response

    def list_memberships(
        self,
        membership_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        active: Optional[bool] = None,
        version: Literal["v1", "v2"] = "v2",
    ) -> List[ContratosResumoApiViewModel]:
        """List all memberships."""
        response = self.get_memberships(
            membership_id=membership_id,
            name=name,
            branch_id=branch_id,
            take=take,
            skip=skip,
            active=active,
            version=version,
            async_req=False,
        )
        if isinstance(response, list):
            return response
        elif isinstance(response, ContratosResumoContainerViewModel) and response.list:
            return response.list
        else:
            error_message = (
                "Invalid response type: 'list' is missing from the response."
            )
            logger.error(f"{error_message} Response: {response}")
            raise ValueError(error_message)
