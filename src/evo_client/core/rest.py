from typing import Any, Dict, Optional, TypeVar, Union

import requests
from pydantic import BaseModel
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from requests.sessions import Session

from ..core.configuration import Configuration
from ..exceptions.api_exceptions import ApiException
from .response import RESTResponse

T = TypeVar("T", bound=BaseModel)


class RESTClient:
    """Handles low-level REST operations using requests."""

    def __init__(
        self,
        configuration: Configuration,
        pools_size: int = 4,
        maxsize: Optional[int] = None,
    ):
        self.session = self._create_session(configuration, pools_size, maxsize)
        self.configuration = configuration

    def _create_session(
        self, config: Configuration, pools_size: int, maxsize: Optional[int]
    ) -> Session:
        """Create and configure the requests session."""
        session = requests.Session()

        # Configure SSL
        session.verify = config.ssl_ca_cert or config.verify_ssl
        if config.cert_file and config.key_file:
            session.cert = (config.cert_file, config.key_file)

        # Configure proxy
        if config.proxy:
            session.proxies = {"http": config.proxy, "https": config.proxy}

        # Configure connection pooling
        adapter = HTTPAdapter(
            pool_connections=pools_size,
            pool_maxsize=maxsize or config.connection_pool_maxsize or 4,
        )
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def request(
        self,
        method: str,
        url: str,
        query_params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        body: Optional[Any] = None,
        auth: Optional[HTTPBasicAuth] = None,
        preload_content: bool = True,
        request_timeout: Optional[Union[float, tuple]] = None,
    ) -> RESTResponse:
        """Execute HTTP request with proper error handling."""
        method = method.upper()
        headers = headers or {"Content-Type": "application/json"}
        auth = auth or self.configuration.get_basic_auth_token()

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=query_params,
                headers=headers,
                json=body if isinstance(body, dict) else None,
                data=body if not isinstance(body, dict) else None,
                timeout=self._get_timeout(request_timeout),
                stream=not preload_content,
                auth=auth,
            )

            rest_response = RESTResponse(response)

            if not 200 <= response.status_code <= 299:
                raise ApiException(http_resp=rest_response)

            return rest_response

        except requests.exceptions.RequestException as e:
            raise ApiException(status=0, reason=f"{type(e).__name__}: {str(e)}")

    @staticmethod
    def _get_timeout(
        timeout_value: Optional[Union[float, tuple]],
    ) -> Optional[Union[float, tuple]]:
        """Process timeout value."""
        if timeout_value is None:
            return None
        if isinstance(timeout_value, (int, float)):
            return timeout_value
        if isinstance(timeout_value, tuple) and len(timeout_value) == 2:
            return timeout_value
        raise ValueError("Invalid timeout value")
