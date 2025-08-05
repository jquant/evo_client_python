"""Async HTTP request handler using aiohttp."""

import asyncio
import json
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
)

import aiohttp
from loguru import logger
from pydantic import BaseModel

from ...core.configuration import Configuration

T = TypeVar("T", bound=BaseModel)


class AsyncRequestHandler:
    """Handles async HTTP request preparation and execution using aiohttp."""

    def __init__(self, configuration: Configuration):
        if aiohttp is None:
            raise ImportError(
                "aiohttp is required for async functionality. "
                "Install it with: pip install aiohttp"
            )

        self.configuration = configuration
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self) -> "AsyncRequestHandler":
        """Async context manager entry."""
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.cleanup()

    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Ensure we have an active aiohttp session."""
        if self._session is None or self._session.closed:
            # Create session with proper configuration
            timeout = aiohttp.ClientTimeout(
                total=self.configuration.timeout, connect=30.0  # Connection timeout
            )

            connector = aiohttp.TCPConnector(
                limit=100,  # Total connection pool size
                limit_per_host=30,  # Per-host connection limit
                ssl=self.configuration.verify_ssl,
                enable_cleanup_closed=True,
            )

            self._session = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
                headers=self.configuration.default_headers,
                raise_for_status=False,  # We'll handle status codes manually
            )

        return self._session

    async def cleanup(self) -> None:
        """Cleanup resources."""
        if self._session and not self._session.closed:
            await self._session.close()
            # Wait a bit for the underlying SSL connections to close
            await asyncio.sleep(0.1)

    def _prepare_headers(self, header_params: Optional[Dict] = None) -> Dict:
        """Prepare request headers with authentication."""
        headers = self.configuration.default_headers.copy()
        if header_params:
            headers.update(header_params)
        return headers

    def _prepare_params(self, query_params: Optional[Dict] = None) -> Dict[str, Any]:
        """Prepare query parameters for aiohttp.

        The underlying ``aiohttp`` request builder only accepts ``str``, ``int``
        or ``float`` types. Boolean values must be converted to strings or they
        will raise a ``TypeError`` when building the request.
        """

        if not query_params:
            return {}

        prepared: Dict[str, Any] = {}
        for key, value in query_params.items():
            if value is None:
                continue
            if isinstance(value, bool):
                prepared[key] = str(value).lower()
            else:
                prepared[key] = value

        return prepared

    async def execute(
        self, response_type: Optional[Type[T] | Type[Iterable[T]]] = None, **kwargs
    ) -> Union[T, List[T], Any]:
        """Execute an async request."""
        return await self._make_request(response_type, **kwargs)

    async def _make_request(
        self, response_type: Optional[Type[T] | Type[Iterable[T]]] = None, **kwargs
    ) -> Union[T, List[T], Any]:
        """Make the actual async HTTP request."""
        method = kwargs.get("method", "GET")
        url = self.configuration.host + kwargs.get("resource_path", "")
        raw_response = kwargs.get("raw_response", False)
        _return_http_data_only = kwargs.get("_return_http_data_only", True)

        # Log the full URL and request details
        logger.debug(f"Making async {method} request to {url}")
        logger.debug(f"Host: {self.configuration.host}")
        logger.debug(f"Resource path: {kwargs.get('resource_path', '')}")

        # Prepare request parameters
        headers = self._prepare_headers(kwargs.get("header_params"))
        query_params = self._prepare_params(kwargs.get("query_params"))
        body = kwargs.get("body")

        logger.debug(f"Request headers: {headers}")
        logger.debug(f"Request body: {body}")

        # Prepare authentication
        auth = None
        basic_auth = self.configuration.get_basic_auth_token()
        if basic_auth:
            # Extract username and password from HTTPBasicAuth object
            login = (
                basic_auth.username
                if isinstance(basic_auth.username, str)
                else str(basic_auth.username)
            )
            password = (
                basic_auth.password
                if isinstance(basic_auth.password, str)
                else str(basic_auth.password)
            )
            auth = aiohttp.BasicAuth(login, password)

        # Prepare request data
        data = None
        json_data = None
        if body is not None:
            if isinstance(body, (dict, list)):
                json_data = body
                if "Content-Type" not in headers:
                    headers["Content-Type"] = "application/json"
            else:
                data = body

        session = await self._ensure_session()

        try:
            async with session.request(
                method=method,
                url=url,
                headers=headers,
                params=query_params,
                data=data,
                json=json_data,
                auth=auth,
            ) as response:
                logger.debug(f"Response status: {response.status}")
                logger.debug(f"Response headers: {dict(response.headers)}")

                # Read response data
                response_data = await response.read()
                logger.debug(f"Raw response data length: {len(response_data)}")

                # Create a RESTResponse-like object for compatibility
                rest_response = AsyncRESTResponse(
                    status=response.status,
                    headers=dict(response.headers),
                    data=response_data,
                    url=str(response.url),
                )

                # Return raw response if requested or if it's a non-JSON content type
                content_type = response.headers.get("Content-Type", "")
                if (
                    raw_response
                    or not _return_http_data_only
                    or "application/json" not in content_type.lower()
                ):
                    logger.debug("Returning raw response")
                    return rest_response

                # Check for error status codes
                if response.status >= 400:
                    logger.error(f"Request failed with status {response.status}")
                    try:
                        error_text = response_data.decode("utf-8", errors="replace")
                        logger.error(f"Error response: {error_text}")
                    except Exception:
                        pass

                    # Raise appropriate exception based on status code
                    if response.status == 401:
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message="Unauthorized - check your credentials",
                        )
                    elif response.status == 404:
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message="Resource not found",
                        )
                    else:
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=f"HTTP {response.status} error",
                        )

                # Try to decode response data
                decoded_data = None
                if response_data:
                    try:
                        decoded_data = response_data.decode("utf-8", errors="replace")
                        logger.debug(
                            f"Decoded response: {decoded_data[:500]}..."
                        )  # Log first 500 chars
                    except Exception as e:
                        logger.warning(f"Failed to decode response: {e}")

                # If a specific response type is expected, try to deserialize
                if response_type:
                    try:
                        return rest_response.deserialize(response_type)
                    except Exception as e:
                        logger.warning(f"Failed to deserialize response: {e}")
                        if 200 <= response.status < 300:
                            logger.debug(
                                f"Request succeeded with status {response.status} despite deserialization failure"
                            )
                            return rest_response
                        raise ValueError(f"Failed to deserialize response: {str(e)}")

                # Try to parse as JSON
                try:
                    if decoded_data:
                        return json.loads(decoded_data)
                    return {}
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse response as JSON: {e}")
                    # Return response object for successful status codes even if parsing fails
                    if 200 <= response.status < 300:
                        logger.debug(
                            f"Request succeeded with status {response.status} despite parsing failure"
                        )
                        return rest_response
                    logger.error(f"Request failed with status {response.status}")
                    raise ValueError(f"Failed to parse response: {str(e)}")

        except aiohttp.ClientError as e:
            logger.error(f"HTTP client error: {e}")
            raise
        except asyncio.TimeoutError as e:
            logger.error(f"Request timeout: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in async request: {e}")
            raise


class AsyncRESTResponse:
    """Async-compatible response wrapper that mimics RESTResponse interface."""

    def __init__(self, status: int, headers: Dict[str, str], data: bytes, url: str):
        self.status = status
        self._headers = headers
        self.data = data
        self.url = url

    def getheaders(self) -> Dict[str, str]:
        """Get response headers."""
        return self._headers

    def json(self) -> Any:
        """Parse response as JSON."""
        if isinstance(self.data, bytes):
            text = self.data.decode("utf-8", errors="replace")
        else:
            text = self.data
        return json.loads(text)

    def deserialize(
        self, response_type: Type[T] | Type[Iterable[T]]
    ) -> Union[T, List[T]]:
        """Deserialize response to the specified type."""
        if isinstance(response_type, type) and issubclass(response_type, BaseModel):
            return cast(T, response_type.model_validate(self.json()))

        # Handle generic types like List[SomeBaseModel]
        origin = get_origin(response_type)
        if origin is list:
            item_type = get_args(response_type)[0]
            json_data = self.json()

            # If the response is a single dictionary and we expect a list,
            # wrap it in a list (this handles container responses)
            if isinstance(json_data, dict):
                return cast(List[T], [item_type.model_validate(json_data)])

            # If it's already a list, validate each item
            elif isinstance(json_data, list):
                return cast(
                    List[T], [item_type.model_validate(item) for item in json_data]
                )

            # Fallback: try to iterate over the response
            else:
                return cast(
                    List[T], [item_type.model_validate(item) for item in json_data]
                )

        # Direct construction for simple types
        return cast(Union[T, List[T]], response_type(**self.json()))
