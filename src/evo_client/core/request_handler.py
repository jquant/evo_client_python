import logging
from multiprocessing.pool import AsyncResult, ThreadPool
from typing import Any, Dict, Iterable, List, Optional, Type, TypeVar, Union, overload

from pydantic import BaseModel

from .configuration import Configuration
from .rest import RESTClient

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


class RequestHandler:
    """Handles HTTP request preparation and execution."""

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.pool = ThreadPool()
        self.rest_client = RESTClient(configuration)

    def cleanup(self) -> None:
        """Cleanup resources."""
        self.pool.close()
        self.pool.join()

    @overload
    def execute(self, response_type: None, **kwargs) -> Any: ...

    @overload
    def execute(self, response_type: Type[T], **kwargs) -> T: ...

    @overload
    def execute(self, response_type: Type[Iterable[T]], **kwargs) -> List[T]: ...

    def execute(
        self, response_type: Optional[Type[T] | Type[Iterable[T]]] = None, **kwargs
    ) -> Union[T, List[T], Any]:
        """Execute a synchronous request."""
        return self._make_request(response_type, **kwargs)

    @overload
    def execute_async(self, response_type: None, **kwargs) -> AsyncResult[Any]: ...

    @overload
    def execute_async(self, response_type: Type[T], **kwargs) -> AsyncResult[T]: ...

    @overload
    def execute_async(
        self, response_type: Type[Iterable[T]], **kwargs
    ) -> AsyncResult[List[T]]: ...

    def execute_async(
        self, response_type: Optional[Type[T] | Type[Iterable[T]]] = None, **kwargs
    ) -> Union[AsyncResult[T], AsyncResult[List[T]], AsyncResult[Any]]:
        """Execute an asynchronous request."""
        return self.pool.apply_async(
            self._make_request, args=(response_type,), kwds=kwargs
        )

    def _prepare_headers(self, header_params: Optional[Dict] = None) -> Dict:
        """Prepare request headers with authentication."""
        headers = self.configuration.default_headers.copy()
        if header_params:
            headers.update(header_params)
        return headers

    def _prepare_params(self, query_params: Optional[Dict] = None) -> Dict:
        """Prepare query parameters."""
        return query_params or {}

    def _get_request_options(self, kwargs: Dict) -> Dict:
        """Extract request options from kwargs."""
        return {
            "request_timeout": kwargs.get("timeout", self.configuration.timeout),
            "verify_ssl": kwargs.get("verify", self.configuration.verify_ssl),
        }

    def _make_request(
        self, response_type: Optional[Type[T] | Type[Iterable[T]]] = None, **kwargs
    ) -> Union[T, List[T], Any]:
        """Make the actual HTTP request."""
        method = kwargs.get("method", "GET")
        url = self.configuration.host + kwargs.get("resource_path", "")
        raw_response = kwargs.get("raw_response", False)
        _return_http_data_only = kwargs.get("_return_http_data_only", True)

        # Log the full URL and request details
        logger.debug(f"Making {method} request to {url}")
        logger.debug(f"Host: {self.configuration.host}")
        logger.debug(f"Resource path: {kwargs.get('resource_path', '')}")

        # Prepare request parameters
        headers = self._prepare_headers(kwargs.get("header_params"))
        query_params = self._prepare_params(kwargs.get("query_params"))
        body = kwargs.get("body")

        logger.debug(f"Request headers: {headers}")
        logger.debug(f"Request body: {body}")

        request_options = self._get_request_options(kwargs)
        response = self.rest_client.request(
            method=method,
            url=url,
            headers=headers,
            query_params=query_params,
            body=body,
            auth=self.configuration.get_basic_auth_token(),
            preload_content=True,
            request_timeout=request_options["request_timeout"],
        )

        logger.debug(f"Response status: {response.status}")
        logger.debug(f"Response headers: {response.getheaders()}")
        logger.debug(f"Raw response data: {response.data}")

        # Return raw response if requested or if it's a non-JSON content type
        content_type = response.getheaders().get("Content-Type", "")
        if (
            raw_response
            or not _return_http_data_only
            or "application/json" not in content_type.lower()
        ):
            logger.debug("Returning raw response")
            return response

        # Try to decode response data
        decoded_data = None
        if isinstance(response.data, bytes):
            try:
                decoded_data = response.data.decode("utf-8", errors="replace")
                logger.debug(f"Decoded response: {decoded_data}")
            except Exception as e:
                logger.warning(f"Failed to decode response: {e}")

        # If a specific response type is expected, try to deserialize
        if response_type:
            try:
                return response.deserialize(response_type)
            except Exception as e:
                logger.warning(f"Failed to deserialize response: {e}")
                if 200 <= response.status < 300:
                    logger.debug(
                        f"Request succeeded with status {response.status} despite deserialization failure"
                    )
                    return response
                raise ValueError(f"Failed to deserialize response: {str(e)}")

        # Try to parse as JSON
        try:
            # Try to use the decoded data first if available
            if decoded_data:
                try:
                    import json

                    return json.loads(decoded_data)
                except json.JSONDecodeError:
                    pass

            # Fall back to response's json method
            return response.json()
        except Exception as e:
            logger.warning(f"Failed to parse response as JSON: {e}")
            # Return response object for successful status codes even if parsing fails
            if 200 <= response.status < 300:
                logger.debug(
                    f"Request succeeded with status {response.status} despite parsing failure"
                )
                return response
            logger.error(f"Request failed with status {response.status}")
            raise ValueError(f"Failed to parse response: {str(e)}")
