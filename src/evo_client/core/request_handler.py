from typing import Any, Dict, Optional
from multiprocessing.pool import ThreadPool, AsyncResult
from multiprocessing.pool import AsyncResult
from typing import Any
import logging

from .rest import RESTClient
from ..exceptions.api_exceptions import RequestError
from .configuration import Configuration

logger = logging.getLogger(__name__)


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

    def execute(self, **kwargs) -> Any:
        """Execute a synchronous request."""
        try:
            return self._make_request(**kwargs)
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise RequestError(f"Request failed: {str(e)}")

    def execute_async(self, **kwargs) -> AsyncResult[Any]:
        """Execute an asynchronous request."""
        return self.pool.apply_async(self._make_request, kwds=kwargs)

    def _prepare_headers(self, header_params: Optional[Dict] = None) -> Dict:
        """Prepare request headers with authentication."""
        headers = header_params or {}
        encoded_auth = self.configuration.get_basic_auth_token()
        headers["Authorization"] = f"Basic {encoded_auth}"
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

    def _make_request(self, **kwargs) -> Any:
        """Make the actual HTTP request."""
        method = kwargs.get("method", "GET")
        url = self.configuration.host + kwargs.get("resource_path", "")

        # Prepare request parameters
        headers = self._prepare_headers(kwargs.get("header_params"))
        query_params = self._prepare_params(kwargs.get("query_params"))
        body = kwargs.get("body")

        logger.debug(f"Making {method} request to {url}")

        request_options = self._get_request_options(kwargs)
        response = self.rest_client.request(
            method=method,
            url=url,
            headers=headers,
            query_params=query_params,
            body=body,
            preload_content=True,
            request_timeout=request_options["request_timeout"],
        )

        logger.debug(f"Received response: {response.status}")
        return response
