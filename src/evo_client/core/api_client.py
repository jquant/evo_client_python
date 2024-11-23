from __future__ import annotations
from typing import Optional, Dict, Any, Union, List, Type, overload
import logging
from multiprocessing.pool import AsyncResult
from typing import Any
from functools import lru_cache
from typing import TypeVar
from .serializer import Serializer
from .request_handler import RequestHandler
from .configuration import Configuration
from ..exceptions.api_exceptions import ApiClientError
from multiprocessing.pool import AsyncResult

logger = logging.getLogger(__name__)


T = TypeVar("T")


class ApiClient:
    """Modern API client for Swagger-generated services."""

    def __init__(
        self,
        configuration: Optional[Configuration] = None,
        header_name: Optional[str] = None,
        header_value: Optional[str] = None,
        cookie: Optional[str] = None,
    ):
        self.configuration = configuration or Configuration()
        self.validate_configuration()

        self.serializer = Serializer()
        self.request_handler = RequestHandler(self.configuration)

        # Initialize headers
        self.default_headers = {}
        if header_name:
            self.default_headers[header_name] = header_value
        self.cookie = cookie
        self.user_agent = "Swagger-Codegen/1.0.0/python"

    def __enter__(self) -> ApiClient:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.request_handler.cleanup()

    @property
    def user_agent(self) -> str:
        return self.default_headers["User-Agent"]

    @user_agent.setter
    def user_agent(self, value: str) -> None:
        self.default_headers["User-Agent"] = value

    def validate_configuration(self) -> None:
        if not self.configuration.host:
            raise ApiClientError("Host URL is required")

    @overload
    def call_api(
        self,
        resource_path: str,
        method: str,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, str]] = None,
        response_type: Optional[Type[T]] = None,
        auth_settings: Optional[List[str]] = None,
        async_req: bool = True,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[float, tuple]] = None,
    ) -> AsyncResult[Any]: ...

    @overload
    def call_api(
        self,
        resource_path: str,
        method: str,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, str]] = None,
        response_type: Optional[Type[T]] = None,
        auth_settings: Optional[List[str]] = None,
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[float, tuple]] = None,
    ) -> Any: ...

    def call_api(
        self,
        resource_path: str,
        method: str,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, str]] = None,
        response_type: Optional[Type[T]] = None,
        auth_settings: Optional[List[str]] = None,
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[float, tuple]] = None,
    ) -> Union[T, AsyncResult[Any]]:
        """
        Makes the HTTP request (synchronous or asynchronous) and returns deserialized data.
        """
        try:
            return self._execute_request(
                resource_path=resource_path,
                method=method,
                path_params=path_params,
                query_params=query_params,
                headers=headers,
                body=body,
                post_params=post_params,
                files=files,
                response_type=response_type,
                auth_settings=auth_settings,
                async_req=async_req,
                _return_http_data_only=_return_http_data_only,
                _preload_content=_preload_content,
                _request_timeout=_request_timeout,
            )
        except Exception as e:
            logger.error(f"API call failed: {str(e)}")
            raise

    @overload
    def _execute_request(
        self, *, async_req: bool = True, **kwargs
    ) -> AsyncResult[Any]: ...

    @overload
    def _execute_request(self, *, async_req: bool = False, **kwargs) -> Any: ...

    def _execute_request(
        self, *, async_req: bool = True, **kwargs
    ) -> Union[Any, AsyncResult[Any]]:
        """Execute the request with caching for GET requests."""
        if kwargs["method"].upper() == "GET":
            # Only cache GET requests using a tuple of relevant parameters
            cache_key = (
                kwargs["resource_path"],
                tuple(sorted(kwargs.get("query_params", {}).items())),
                tuple(sorted(kwargs.get("headers", {}).items())),
            )
            return self._cached_get_request(cache_key, **kwargs)

        if async_req:
            return self.request_handler.execute_async(**kwargs)
        return self.request_handler.execute(**kwargs)

    @lru_cache(maxsize=128)
    def _cached_get_request(self, cache_key: tuple, **kwargs) -> Any:
        """Cached wrapper for GET requests."""
        if kwargs["async_req"]:
            return self.request_handler.execute_async(**kwargs)
        return self.request_handler.execute(**kwargs)
