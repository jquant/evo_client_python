"""Clean synchronous States API."""

from typing import Any

from .base import SyncBaseApi


class SyncStatesApi(SyncBaseApi):
    """Clean synchronous States API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/states"

    def get_states(self) -> Any:
        """
        Get list of available states/provinces.

        Returns:
            List of state objects containing details like:
            - State ID and name
            - State abbreviation/code
            - Country information
            - Regional data

        Example:
            >>> with SyncStatesApi() as api:
            ...     states = api.get_states()
            ...     for state in states:
            ...         print(f"State: {state.name} ({state.abbreviation})")
            ...         print(f"Country: {state.country}")
        """
        result = self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            response_type=None,
            headers={"Accept": ["text/plain", "application/json", "text/json"]},
            auth_settings=["Basic"],
        )
        return result
