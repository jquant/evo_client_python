# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401
from datetime import datetime
from multiprocessing.pool import AsyncResult
from typing import Any, List, Literal, Optional, Union, overload, cast
from loguru import logger

from evo_client.core.api_client import ApiClient

from ..models.entradas_resumo_api_view_model import EntradasResumoApiViewModel

# python 2 and python 3 compatibility library


class EntriesApi:
    """Entries API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/entries"
        self.logger = logger

    @overload
    def get_entries(
        self,
        *,
        async_req: Literal[False] = False,
        register_date_start: Optional[datetime] = None,
        register_date_end: Optional[datetime] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        entry_id: Optional[int] = None,
        member_id: Optional[int] = None,
    ) -> List[EntradasResumoApiViewModel]:
        ...

    @overload
    def get_entries(
        self,
        *,
        async_req: Literal[True],
        register_date_start: Optional[datetime] = None,
        register_date_end: Optional[datetime] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        entry_id: Optional[int] = None,
        member_id: Optional[int] = None,
    ) -> AsyncResult[Any]:
        ...

    def get_entries(
        self,
        *,
        register_date_start: Optional[datetime] = None,
        register_date_end: Optional[datetime] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        entry_id: Optional[int] = None,
        member_id: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[List[EntradasResumoApiViewModel], AsyncResult[Any]]:
        """
        Get entries with optional filtering.

        Args:
            register_date_start: DateTime date start
            register_date_end: DateTime date end
            take: Total number of records to return (Maximum of 1000)
            skip: Total number of records to skip
            entry_id: ID of the entry to return
            member_id: ID of the member to return
            async_req: Execute request asynchronously

        Returns:
            List of entries or AsyncResult if async

        Raises:
            ValueError: If take > 1000
        """
        self.logger.debug(
            "Starting entries API call [start={}, end={}, take={}, skip={}, entry_id={}, member_id={}]",
            register_date_start, register_date_end, take, skip, entry_id, member_id
        )
        start_time = datetime.now()

        if take and take > 1000:
            raise ValueError("Maximum number of records to return is 1000")

        params = {
            "registerDateStart": register_date_start,
            "registerDateEnd": register_date_end,
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
            async_req=async_req,
            headers={"Accept": "application/json"},
        )
        
        elapsed_time = (datetime.now() - start_time).total_seconds()
        self.logger.info("Entries API call completed in {:.2f}s", elapsed_time)
        return result

    @overload
    def get_member_entries(
        self,
        member_id: int,
        *,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        async_req: bool = False,
    ) -> List[EntradasResumoApiViewModel]:
        ...

    @overload
    def get_member_entries(
        self,
        member_id: int,
        *,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        async_req: bool = False,
    ) -> AsyncResult[Any]:
        ...

    def get_member_entries(
        self,
        member_id: int,
        *,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        async_req: bool = False,
    ) -> Union[List[EntradasResumoApiViewModel], AsyncResult[Any]]:
        """
        Get entries for a specific member.

        Args:
            member_id: ID of the member to get entries for
            start_date: Start date filter
            end_date: End date filter
            async_req: Execute request asynchronously

        Returns:
            List of entries or AsyncResult if async
        """
        if async_req:
            return self.get_entries(
                member_id=member_id,
                register_date_start=start_date,
                register_date_end=end_date,
                async_req=True,
            )
        return self.get_entries(
            member_id=member_id,
            register_date_start=start_date,
            register_date_end=end_date,
            async_req=False,
        )

    @overload
    def get_entry_by_id(
        self,
        entry_id: int,
        *,
        async_req: Literal[False] = False,
    ) -> Optional[EntradasResumoApiViewModel]:
        ...

    @overload
    def get_entry_by_id(
        self,
        entry_id: int,
        *,
        async_req: Literal[True],
    ) -> AsyncResult[Any]:
        ...

    def get_entry_by_id(
        self,
        entry_id: int,
        *,
        async_req: bool = False,
    ) -> Union[Optional[EntradasResumoApiViewModel], AsyncResult[Any]]:
        """
        Get a specific entry by ID.

        Args:
            entry_id: ID of the entry to get
            async_req: Execute request asynchronously

        Returns:
            Entry if found, None if not found, or AsyncResult if async
        """
        if async_req:
            result = self.get_entries(
                entry_id=entry_id,
                async_req=True,
            )
            return result
        result = self.get_entries(
            entry_id=entry_id,
            async_req=False,
        )
        return result[0] if result else None    