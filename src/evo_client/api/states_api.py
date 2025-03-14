from multiprocessing.pool import AsyncResult
from typing import Any, Literal, Optional, Union, overload

from ..core.api_client import ApiClient
from .base import BaseApi


class StatesApi(BaseApi):
    """States API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        super().__init__(api_client)
        self.base_path = "/api/v1/states"

    @overload
    def get_states(self, async_req: Literal[False] = False) -> Any:
        ...

    @overload
    def get_states(self, async_req: Literal[True] = True) -> AsyncResult[Any]:
        ...

    def get_states(self, async_req: bool = False) -> Union[Any, AsyncResult[Any]]:
        """
        Get list of available states/provinces.

        Args:
            async_req: Execute request asynchronously

        Returns:
            List of state objects containing details like:
            - State ID
            - State name
            - State abbreviation
            - Country information
        """
        return self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            response_type=None,
            headers={"Accept": ["text/plain", "application/json", "text/json"]},
            auth_settings=["Basic"],
            async_req=async_req,
        )
