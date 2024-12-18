from ..core.api_client import ApiClient
from typing import Optional


class BaseApi:
    """Base class for all API classes."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
