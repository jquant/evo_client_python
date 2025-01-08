from multiprocessing.pool import AsyncResult
from typing import Any, List, Literal, Optional, Union, overload

from ..core.api_client import ApiClient
from ..models.servicos_resumo_api_view_model import ServicosResumoApiViewModel
from .base import BaseApi


class ServiceApi(BaseApi):
    """Service API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        super().__init__(api_client)
        self.base_path = "/api/v1/service"

    @overload
    def get_services(
        self,
        service_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        active: Optional[bool] = None,
        async_req: Literal[False] = False,
    ) -> List[ServicosResumoApiViewModel]:
        ...

    @overload
    def get_services(
        self,
        service_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        active: Optional[bool] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]:
        ...

    def get_services(
        self,
        service_id: Optional[int] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        active: Optional[bool] = None,
        async_req: bool = False,
    ) -> Union[List[ServicosResumoApiViewModel], AsyncResult[Any]]:
        """
        Get services list with optional filtering.

        Args:
            service_id: Filter by Service Id
            name: Filter by service name
            branch_id: Filter by service branch ID (Only for multilocation key)
            take: Total number of records to return (Maximum of 50)
            skip: Total number of records to skip
            active: Filter by active/inactive services
            async_req: Execute request asynchronously
        """
        params = {
            "idService": service_id,
            "name": name,
            "idBranch": branch_id,
            "take": take,
            "skip": skip,
            "active": active,
        }

        return self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[ServicosResumoApiViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
        )
