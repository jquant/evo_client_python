"""Clean synchronous HTTP request handler."""

from typing import Any, Dict, Iterable, List, Optional, Type, TypeVar, Union

from loguru import logger
from pydantic import BaseModel

from ...core.configuration import Configuration
from ...core.rest import RESTClient

T = TypeVar("T", bound=BaseModel)


class SyncRequestHandler:
    """Handles synchronous HTTP request preparation and execution."""

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.rest_client = RESTClient(configuration)

    def cleanup(self) -> None:
        """Cleanup resources."""
        # No thread pool to clean up in sync version

    def execute(
        self, response_type: Optional[Type[T] | Type[Iterable[T]]] = None, **kwargs
    ) -> Union[T, List[T], Any]:
        """Execute a synchronous request."""
        return self._make_request(response_type, **kwargs)

    def _prepare_headers(self, header_params: Optional[Dict] = None) -> Dict:
        """Prepare request headers with authentication."""
        headers = self.configuration.default_headers.copy()
        if header_params:
            headers.update(header_params)
        return headers

    def _prepare_params(self, query_params: Optional[Dict] = None) -> Dict:
        """Prepare query parameters.

        Boolean values are converted to lowercase strings so that sync and async
        implementations behave the same when sending query parameters.
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

        try:
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

            return self._process_response(
                response, response_type, raw_response, _return_http_data_only
            )

        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise

    def _process_response(
        self, response, response_type, raw_response: bool, _return_http_data_only: bool
    ) -> Union[T, List[T], Any]:
        """Process the HTTP response."""
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
