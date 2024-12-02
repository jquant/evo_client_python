from datetime import datetime
from multiprocessing.pool import AsyncResult
from typing import Any, List, Literal, Optional, Union, overload

from ..core.api_client import ApiClient
from ..models.convenios_api_view_model import ConveniosApiViewModel


class PartnershipApi:
    """Partnership API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/partnership"

    @overload
    def get_partnerships(
        self,
        status: Optional[int] = None,
        description: Optional[str] = None,
        dt_created: Optional[datetime] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]:
        ...

    @overload
    def get_partnerships(
        self,
        status: Optional[int] = None,
        description: Optional[str] = None,
        dt_created: Optional[datetime] = None,
        async_req: Literal[False] = False,
    ) -> List[ConveniosApiViewModel]:
        ...

    def get_partnerships(
        self,
        status: Optional[int] = None,
        description: Optional[str] = None,
        dt_created: Optional[datetime] = None,
        async_req: bool = False,
    ) -> Union[List[ConveniosApiViewModel], AsyncResult[Any]]:
        """
        Get partnerships with optional filtering.

        Args:
            status: Filter by status: 0=Both, 1=Active, 2=Inactive
            description: Filter by partnership name
            dt_created: Filter by registration date
            async_req: Execute request asynchronously
        """
        params = {
            "status": status,
            "description": description,
            "dtCreated": dt_created,
        }

        return self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[ConveniosApiViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
        )
