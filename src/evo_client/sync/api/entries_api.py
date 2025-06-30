"""Clean synchronous Entries API."""

from datetime import datetime
from typing import List, Optional, cast

from loguru import logger

from ...models.entradas_resumo_api_view_model import EntradasResumoApiViewModel
from .base import SyncBaseApi


class SyncEntriesApi(SyncBaseApi):
    """Clean synchronous Entries API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/entries"
        self.logger = logger

    def get_entries(
        self,
        register_date_start: Optional[datetime] = None,
        register_date_end: Optional[datetime] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        entry_id: Optional[int] = None,
        member_id: Optional[int] = None,
    ) -> List[EntradasResumoApiViewModel]:
        """
        Get entries with optional filtering.

        Args:
            register_date_start: DateTime date start
            register_date_end: DateTime date end
            take: Total number of records to return (Maximum of 1000)
            skip: Total number of records to skip
            entry_id: ID of the entry to return
            member_id: ID of the member to return

        Returns:
            List of entries

        Raises:
            ValueError: If take > 1000

        Example:
            >>> with SyncEntriesApi() as api:
            ...     entries = api.get_entries(
            ...         register_date_start=datetime(2024, 1, 1),
            ...         register_date_end=datetime(2024, 12, 31),
            ...         take=100
            ...     )
            ...     for entry in entries:
            ...         print(f"Entry {entry.id} - Member: {entry.member_id}")
        """
        self.logger.debug(
            "Starting entries API call [start={}, end={}, take={}, skip={}, entry_id={}, member_id={}]",
            register_date_start,
            register_date_end,
            take,
            skip,
            entry_id,
            member_id,
        )
        start_time = datetime.now()

        if take and take > 1000:
            raise ValueError("Maximum number of records to return is 1000")

        params = {
            "registerDateStart": (
                register_date_start.isoformat() if register_date_start else None
            ),
            "registerDateEnd": (
                register_date_end.isoformat() if register_date_end else None
            ),
            "take": take,
            "skip": skip,
            "IdEntry": entry_id,
            "idMember": member_id,
        }

        result = self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[EntradasResumoApiViewModel],
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )

        elapsed_time = (datetime.now() - start_time).total_seconds()
        self.logger.info("Entries API call completed in {:.2f}s", elapsed_time)
        return cast(List[EntradasResumoApiViewModel], result)
