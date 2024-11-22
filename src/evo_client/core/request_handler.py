from typing import Any, Dict, Optional
from multiprocessing.pool import ThreadPool, AsyncResult
from threading import Thread
import logging

from .rest import RESTClient
from ..exceptions.api_exceptions import RequestError


logger = logging.getLogger(__name__)


class RequestHandler:
    """Handles HTTP request preparation and execution."""

    def __init__(self, configuration):
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
        """Prepare request headers."""
        return header_params or {}

    def _prepare_params(self, query_params: Optional[Dict] = None) -> Dict:
        """Prepare query parameters."""
        return query_params or {}

    def _get_request_options(self, kwargs: Dict) -> Dict:
        """Extract request options from kwargs."""
        return {
            "timeout": kwargs.get("timeout", self.configuration.timeout),
            "verify": kwargs.get("verify", self.configuration.verify_ssl),
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

        response = self.rest_client.request(
            method=method,
            url=url,
            headers=headers,
            query_params=query_params,
            body=body,
            **self._get_request_options(kwargs)
        )

        logger.debug(f"Received response: {response.status}")
        return response
