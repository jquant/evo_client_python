"""Clean synchronous API client."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Type, TypeVar, Union, overload

from pydantic import BaseModel

from ...core.configuration import Configuration
from .request_handler import SyncRequestHandler

T = TypeVar("T", bound=BaseModel)


class SyncApiClient:
    """Clean synchronous API client for EVO services."""

    def __init__(
        self,
        configuration: Optional[Configuration] = None,
        header_name: Optional[str] = None,
        header_value: Optional[str] = None,
        cookie: Optional[str] = None,
    ):
        self.configuration = configuration or Configuration()

        self.request_handler = SyncRequestHandler(self.configuration)

        # Initialize headers
        self.default_headers: Dict[str, str | None] = {}
        if header_name:
            self.default_headers[header_name] = header_value
        self.cookie = cookie
        self.user_agent = "EVO-Client-Python/2.0.0/sync"

    def __enter__(self) -> SyncApiClient:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.request_handler.cleanup()

    @property
    def user_agent(self) -> str:
        return self.default_headers["User-Agent"] or ""

    @user_agent.setter
    def user_agent(self, value: str) -> None:
        self.default_headers["User-Agent"] = value

    # Overloads for better typing support
    @overload
    def call_api(
        self,
        resource_path: str,
        method: str,
        *,
        response_type: None = None,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, str]] = None,
        auth_settings: Optional[List[str]] = None,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[float, tuple]] = None,
        raw_response: bool = False,
    ) -> Any:
        ...

    @overload
    def call_api(
        self,
        resource_path: str,
        method: str,
        *,
        response_type: Type[T],
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, str]] = None,
        auth_settings: Optional[List[str]] = None,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[float, tuple]] = None,
        raw_response: bool = False,
    ) -> T:
        ...

    @overload
    def call_api(
        self,
        resource_path: str,
        method: str,
        *,
        response_type: Type[List[T]],
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, str]] = None,
        auth_settings: Optional[List[str]] = None,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[float, tuple]] = None,
        raw_response: bool = False,
    ) -> List[T]:
        ...

    @overload
    def call_api(
        self,
        resource_path: str,
        method: str,
        *,
        response_type: Optional[Type[T] | Type[Iterable[T]]] = None,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, str]] = None,
        auth_settings: Optional[List[str]] = None,
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[float, tuple]] = None,
        raw_response: bool = True,
    ) -> Any:
        ...

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
        _return_http_data_only: bool = True,
        _preload_content: bool = True,
        _request_timeout: Optional[Union[float, tuple]] = None,
        raw_response: bool = False,
    ) -> Union[T, List[T], Any]:
        """
        Makes a synchronous HTTP request and returns deserialized data.

        Args:
            resource_path: The resource path for the API endpoint
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            response_type: Expected response type for deserialization
            path_params: Path parameters to substitute in the URL
            query_params: Query parameters to append to the URL
            headers: Additional headers to send with the request
            body: Request body data
            post_params: Form parameters for POST requests
            files: Files to upload
            auth_settings: Authentication settings to use
            _return_http_data_only: Whether to return only HTTP data
            _preload_content: Whether to preload response content
            _request_timeout: Request timeout (seconds)
            raw_response: If True, returns the raw response object

        Returns:
            Deserialized response data of the specified type

        Example:
            >>> client = SyncApiClient()
            >>> # Type-safe: returns List[MemberViewModel]
            >>> members = client.call_api(
            ...     resource_path="/api/v1/members",
            ...     method="GET",
            ...     response_type=List[MemberViewModel]
            ... )
            >>>
            >>> # Type-safe: returns MemberViewModel
            >>> member = client.call_api(
            ...     resource_path="/api/v1/members/123",
            ...     method="GET",
            ...     response_type=MemberViewModel
            ... )
            >>>
            >>> # Returns Any when no response_type specified
            >>> result = client.call_api("/api/v1/status", "GET")
        """
        if raw_response:
            _return_http_data_only = False
            _preload_content = False

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
            raw_response=raw_response,
        )
