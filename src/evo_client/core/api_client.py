from __future__ import annotations

from multiprocessing.pool import AsyncResult
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Type,
    TypeVar,
    Union,
    overload,
)

from pydantic import BaseModel

from .configuration import Configuration
from .request_handler import RequestHandler


T = TypeVar("T", bound=BaseModel)


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

    @overload
    def call_api(
        self,
        resource_path: str,
        method: str,
        response_type: None = None,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, str]] = None,
        auth_settings: Optional[List[str]] = None,
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[float, tuple]] = None,
        raw_response: bool = False,
    ) -> Union[Any, AsyncResult[Any]]: ...

    @overload
    def call_api(
        self,
        resource_path: str,
        method: str,
        response_type: Type[T],
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, str]] = None,
        auth_settings: Optional[List[str]] = None,
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[float, tuple]] = None,
        raw_response: bool = False,
    ) -> Union[T, AsyncResult[T]]: ...

    @overload
    def call_api(
        self,
        resource_path: str,
        method: str,
        response_type: Type[Iterable[T]],
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, str]] = None,
        auth_settings: Optional[List[str]] = None,
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[float, tuple]] = None,
        raw_response: bool = False,
    ) -> Union[List[T], AsyncResult[List[T]]]: ...

    @overload
    def call_api(
        self,
        resource_path: str,
        method: str,
        response_type: Optional[Type[T] | Type[Iterable[T]]] = None,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, str]] = None,
        auth_settings: Optional[List[str]] = None,
        async_req: Literal[True] = True,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[float, tuple]] = None,
        raw_response: bool = False,
    ) -> Union[AsyncResult[T], AsyncResult[List[T]], AsyncResult[Any]]: ...

    @overload
    def call_api(
        self,
        resource_path: str,
        method: str,
        response_type: Optional[Type[T] | Type[Iterable[T]]] = None,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, str]] = None,
        auth_settings: Optional[List[str]] = None,
        async_req: Literal[False] = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[float, tuple]] = None,
        raw_response: bool = False,
    ) -> Union[T, List[T], Any]: ...

    def call_api(
        self,
        resource_path: str,
        method: str,
        response_type: Optional[Type[T] | Type[Iterable[T]]] = None,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, str]] = None,
        auth_settings: Optional[List[str]] = None,
        async_req: bool = False,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[float, tuple]] = None,
        raw_response: bool = False,
    ) -> Union[T, List[T], Any, AsyncResult[T], AsyncResult[List[T]], AsyncResult[Any]]:
        """
        Makes the HTTP request (synchronous or asynchronous) and returns deserialized data.

        Args:
            ...
            raw_response: If True, returns the raw response object (useful for binary data, Excel files, etc.)
        """
        if raw_response:
            _return_http_data_only = False
            _preload_content = False

        if async_req:
            return self.request_handler.execute_async(
                response_type=response_type,
                resource_path=resource_path,
                method=method,
                path_params=path_params,
                query_params=query_params,
                headers=headers,
                body=body,
                post_params=post_params,
                files=files,
                auth_settings=auth_settings,
                _return_http_data_only=_return_http_data_only,
                _preload_content=_preload_content,
                _request_timeout=_request_timeout,
            )

        return self.request_handler.execute(
            response_type=response_type,
            resource_path=resource_path,
            method=method,
            path_params=path_params,
            query_params=query_params,
            headers=headers,
            body=body,
            post_params=post_params,
            files=files,
            auth_settings=auth_settings,
            _return_http_data_only=_return_http_data_only,
            _preload_content=_preload_content,
            _request_timeout=_request_timeout,
        )
