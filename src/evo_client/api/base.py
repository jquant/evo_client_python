from typing import Optional

from ..core.api_client import ApiClient


class BaseApi:
    """Base class for all API classes."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
