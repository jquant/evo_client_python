from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import requests

from .configuration import Configuration
from .exceptions.api_exceptions import ApiException

T = TypeVar("T")


class ApiClient:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.session = requests.Session()
        if configuration.username and configuration.password:
            self.session.auth = (configuration.username, configuration.password)

    def call_api(
        self,
        path: str,
        method: str,
        query_params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        response_type: Optional[Type[T]] = None,
    ) -> Optional[Union[T, List[T]]]:
        """
        Makes an API call and returns the response

        Args:
            path: API endpoint path
            method: HTTP method (GET, POST, etc.)
            query_params: Query parameters
            body: Request body
            response_type: Expected response type

        Returns:
            Response data converted to specified type
        """
        url = f"{self.configuration.host.rstrip('/')}/{path.lstrip('/')}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=query_params,
                json=body,
                headers={"Content-Type": "application/json"},
            )

            response.raise_for_status()

            if not response_type:
                return None

            data = response.json()

            if isinstance(data, list):
                return [response_type(**item) for item in data]
            return response_type(**data)

        except requests.exceptions.RequestException as e:
            raise ApiException(f"API call failed: {str(e)}")
        except (ValueError, TypeError) as e:
            raise ApiException(f"Failed to parse response: {str(e)}")
