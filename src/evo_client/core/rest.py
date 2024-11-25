from typing import Optional, Dict, Any, Union, Type, TypeVar
import json
import logging
import ssl
from urllib.parse import urlencode

import certifi
import urllib3
from urllib3.response import HTTPResponse, BaseHTTPResponse

from .response import RESTResponse
from ..exceptions.api_exceptions import ApiException
from ..core.configuration import Configuration
from pydantic import BaseModel

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


class RESTClient:
    """Handles low-level REST operations using urllib3."""

    def __init__(
        self,
        configuration: Configuration,
        pools_size: int = 4,
        maxsize: Optional[int] = None,
    ):
        self.pool_manager = self._create_pool_manager(
            configuration, pools_size, maxsize
        )

    def _create_pool_manager(
        self, config: Configuration, pools_size: int, maxsize: Optional[int]
    ) -> Union[urllib3.PoolManager, urllib3.ProxyManager]:
        """Create and configure the appropriate pool manager."""
        cert_reqs = ssl.CERT_REQUIRED if config.verify_ssl else ssl.CERT_NONE
        ca_certs = config.ssl_ca_cert or certifi.where()

        pool_args = {
            "num_pools": pools_size,
            "maxsize": maxsize or config.connection_pool_maxsize or 4,
            "cert_reqs": cert_reqs,
            "ca_certs": ca_certs,
            "cert_file": config.cert_file,
            "key_file": config.key_file,
        }

        if config.assert_hostname is not None:
            pool_args["assert_hostname"] = config.assert_hostname

        return (
            urllib3.ProxyManager(proxy_url=config.proxy, **pool_args)
            if config.proxy
            else urllib3.PoolManager(**pool_args)
        )

    def request(
        self,
        method: str,
        url: str,
        query_params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        body: Optional[Any] = None,
        preload_content: bool = True,
        request_timeout: Optional[Union[float, tuple]] = None,
    ) -> RESTResponse:
        """Execute HTTP request with proper error handling."""
        method = method.upper()
        headers = headers or {"Content-Type": "application/json"}

        try:
            response = self._execute_request(
                method=method,
                url=url,
                query_params=query_params,
                headers=headers,
                body=body,
                preload_content=preload_content,
                timeout=self._get_timeout(request_timeout),
            )

            if not isinstance(response, RESTResponse):
                response = RESTResponse(response)

            if preload_content:
                logger.debug("Response body: %s", response.data)

            if not 200 <= response.status <= 299:
                raise ApiException(http_resp=response)

            return response

        except urllib3.exceptions.SSLError as e:
            raise ApiException(status=0, reason=f"{type(e).__name__}: {str(e)}")

    def _execute_request(self, method: str, url: str, **kwargs) -> BaseHTTPResponse:
        """Execute the actual HTTP request based on method type."""
        if method in ["POST", "PUT", "PATCH", "OPTIONS", "DELETE"]:
            return self._execute_request_with_body(method, url, **kwargs)
        return self._execute_get_request(method, url, **kwargs)

    def _execute_request_with_body(
        self,
        method: str,
        url: str,
        query_params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        body: Optional[Any] = None,
        post_params: Optional[Dict] = None,
        **kwargs
    ) -> BaseHTTPResponse:
        """Handle requests that may include a body."""
        if query_params:
            url += "?" + urlencode(query_params)

        headers = headers or {}
        content_type = headers.get("Content-Type", "").lower()

        if "json" in content_type:
            return self._handle_json_request(method, url, headers, body, **kwargs)
        elif content_type == "application/x-www-form-urlencoded":
            return self._handle_form_request(
                method, url, headers, post_params or {}, False, **kwargs
            )
        elif content_type == "multipart/form-data":
            headers.pop("Content-Type", None)
            return self._handle_form_request(
                method, url, headers, post_params or {}, True, **kwargs
            )
        elif isinstance(body, str):
            return self.pool_manager.request(
                method, url, body=body, headers=headers, **kwargs
            )
        elif isinstance(body, dict):
            return self._handle_json_request(method, url, headers, body, **kwargs)

        raise ApiException(
            status=0, reason="Cannot prepare request message for provided arguments."
        )

    def _handle_json_request(
        self, method: str, url: str, headers: Dict, body: Any, **kwargs
    ) -> BaseHTTPResponse:
        """Handle JSON requests."""
        request_body = json.dumps(body) if body is not None else "{}"
        return self.pool_manager.request(
            method, url, body=request_body, headers=headers, **kwargs
        )

    def _handle_form_request(
        self,
        method: str,
        url: str,
        headers: Dict,
        fields: Dict,
        encode_multipart: bool,
        **kwargs
    ) -> BaseHTTPResponse:
        """Handle form-encoded requests."""
        return self.pool_manager.request(
            method,
            url,
            fields=fields,
            encode_multipart=encode_multipart,
            headers=headers,
            **kwargs
        )

    def _execute_get_request(
        self,
        method: str,
        url: str,
        query_params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> BaseHTTPResponse:
        """Handle GET and HEAD requests."""
        return self.pool_manager.request(
            method, url, fields=query_params, headers=headers, **kwargs
        )

    @staticmethod
    def _get_timeout(
        timeout_value: Optional[Union[float, tuple]]
    ) -> Optional[urllib3.Timeout]:
        """Convert timeout value to urllib3.Timeout object."""
        if timeout_value is None:
            return None
        if isinstance(timeout_value, (int, float)):
            return urllib3.Timeout(total=timeout_value)
        if isinstance(timeout_value, tuple) and len(timeout_value) == 2:
            return urllib3.Timeout(connect=timeout_value[0], read=timeout_value[1])
        raise ValueError("Invalid timeout value")
