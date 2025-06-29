"""Async API client for EVO API."""

from typing import Any, Dict, Iterable, List, Optional, Type, TypeVar, Union

from loguru import logger
from pydantic import BaseModel

from ...core.configuration import Configuration
from .request_handler import AsyncRequestHandler

T = TypeVar("T", bound=BaseModel)


class AsyncApiClient:
    """Modern async API client for EVO API services."""

    def __init__(
        self,
        configuration: Optional[Configuration] = None,
        header_name: Optional[str] = None,
        header_value: Optional[str] = None,
        cookie: Optional[str] = None,
    ):
        """
        Initialize the async API client.

        Args:
            configuration: Optional configuration. If not provided, creates a new one.
            header_name: Optional custom header name.
            header_value: Optional custom header value.
            cookie: Optional cookie value.
        """
        self.configuration = configuration or Configuration()
        self.request_handler = AsyncRequestHandler(self.configuration)

        # Initialize headers
        self.default_headers = {}
        if header_name:
            self.default_headers[header_name] = header_value
        self.cookie = cookie
        self.user_agent = "EVO-Client-Python-Async/1.0.0"

    async def __aenter__(self) -> "AsyncApiClient":
        """Async context manager entry."""
        await self.request_handler.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.request_handler.__aexit__(exc_type, exc_val, exc_tb)

    @property
    def user_agent(self) -> str:
        """Get the user agent string."""
        return self.default_headers["User-Agent"]

    @user_agent.setter
    def user_agent(self, value: str) -> None:
        """Set the user agent string."""
        self.default_headers["User-Agent"] = value

    async def call_api(
        self,
        resource_path: str,
        method: str = "GET",
        response_type: Optional[Type[T] | Type[Iterable[T]]] = None,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        post_params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, str]] = None,
        auth_settings: Optional[List[str]] = None,
        return_http_data_only: bool = True,
        preload_content: bool = True,
        request_timeout: Optional[Union[float, tuple]] = None,
        raw_response: bool = False,
    ) -> Union[T, List[T], Any]:
        """
        Make an async HTTP request and return deserialized data.

        Args:
            resource_path: The API endpoint path (e.g., "/api/v1/members")
            method: HTTP method ("GET", "POST", "PUT", "DELETE", etc.)
            response_type: Expected response type for deserialization
            path_params: Path parameters to substitute in resource_path
            query_params: Query parameters to append to URL
            headers: Additional headers to send
            body: Request body data
            post_params: Form data parameters
            files: Files to upload
            auth_settings: Authentication settings to use
            return_http_data_only: If True, returns only the data part
            preload_content: If True, preloads the response content
            request_timeout: Request timeout override
            raw_response: If True, returns the raw response object

        Returns:
            Deserialized response data or raw response object

        Example:
            >>> async with AsyncApiClient(config) as client:
            ...     members = await client.call_api(
            ...         "/api/v1/members",
            ...         method="GET",
            ...         response_type=List[MemberViewModel],
            ...         query_params={"take": 10}
            ...     )
        """
        logger.debug(f"Making async API call: {method} {resource_path}")

        # Handle path parameters
        if path_params:
            for param, value in path_params.items():
                resource_path = resource_path.replace(f"{{{param}}}", str(value))

        # Prepare headers
        request_headers = self.default_headers.copy()
        if headers:
            request_headers.update(headers)

        # Handle authentication
        if auth_settings:
            auth_config = self.configuration.auth_settings()
            for auth_type in auth_settings:
                if auth_type in auth_config:
                    auth_info = auth_config[auth_type]
                    if auth_info["type"] == "basic":
                        # Basic auth is handled by the request handler
                        pass
                    elif auth_info["type"] == "api_key":
                        # Add API key to headers
                        if auth_info.get("value"):
                            request_headers[auth_info["key"]] = auth_info["value"]

        return await self.request_handler.execute(
            response_type=response_type,
            resource_path=resource_path,
            method=method,
            header_params=request_headers,
            query_params=query_params,
            body=body,
            post_params=post_params,
            files=files,
            _return_http_data_only=return_http_data_only,
            _preload_content=preload_content,
            timeout=request_timeout,
            raw_response=raw_response,
        )
