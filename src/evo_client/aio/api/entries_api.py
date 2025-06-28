"""Clean asynchronous Entries API."""

from datetime import datetime
from typing import List, Optional, cast

from loguru import logger

from ...models.entradas_resumo_api_view_model import EntradasResumoApiViewModel
from .base import AsyncBaseApi


class AsyncEntriesApi(AsyncBaseApi):
    """Clean asynchronous Entries API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/entries"
        self.logger = logger

    async def get_entries(
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
            >>> async with AsyncEntriesApi() as api:
            ...     entries = await api.get_entries(
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

        result = await self.api_client.call_api(
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

    async def get_member_entries(
        self,
        member_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[EntradasResumoApiViewModel]:
        """
        Get entries for a specific member.

        Args:
            member_id: ID of the member to get entries for
            start_date: Start date filter
            end_date: End date filter

        Returns:
            List of entries for the specified member

        Example:
            >>> async with AsyncEntriesApi() as api:
            ...     entries = await api.get_member_entries(
            ...         member_id=12345,
            ...         start_date=datetime(2024, 1, 1),
            ...         end_date=datetime(2024, 12, 31)
            ...     )
            ...     print(f"Member has {len(entries)} entries")
        """
        return await self.get_entries(
            member_id=member_id,
            register_date_start=start_date,
            register_date_end=end_date,
        )

    async def get_entry_by_id(
        self,
        entry_id: int,
    ) -> Optional[EntradasResumoApiViewModel]:
        """
        Get a specific entry by ID.

        Args:
            entry_id: ID of the entry to retrieve

        Returns:
            Entry if found, None otherwise

        Example:
            >>> async with AsyncEntriesApi() as api:
            ...     entry = await api.get_entry_by_id(entry_id=67890)
            ...     if entry:
            ...         print(f"Found entry for member {entry.member_id}")
            ...     else:
            ...         print("Entry not found")
        """
        entries = await self.get_entries(entry_id=entry_id)
        return entries[0] if entries else None
