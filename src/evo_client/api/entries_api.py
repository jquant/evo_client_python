# coding: utf-8

"""
    EVO API

    Use the DNS of your gym as the User and the Secret Key as the password.The authentication method used in the integration is Basic Authentication  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from evo_client.core.api_client import ApiClient

from typing import List, Optional, Union, overload
from datetime import datetime
from threading import Thread

from pydantic import BaseModel

from ..models.entradas_resumo_api_view_model import EntradasResumoApiViewModel


class EntriesApi:
    """Entries API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/entries"

    @overload
    def get_entries(
        self,
        register_date_start: Optional[datetime] = None,
        register_date_end: Optional[datetime] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        entry_id: Optional[int] = None,
        member_id: Optional[int] = None,
        async_req: bool = True,
    ) -> Thread: ...

    @overload
    def get_entries(
        self,
        register_date_start: Optional[datetime] = None,
        register_date_end: Optional[datetime] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        entry_id: Optional[int] = None,
        member_id: Optional[int] = None,
        async_req: bool = False,
    ) -> List[EntradasResumoApiViewModel]: ...

    def get_entries(
        self,
        register_date_start: Optional[datetime] = None,
        register_date_end: Optional[datetime] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        entry_id: Optional[int] = None,
        member_id: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[List[EntradasResumoApiViewModel], Thread]:
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
            List of entries or Thread if async

        Raises:
            ValueError: If take > 1000
        """
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

        return self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[EntradasResumoApiViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def get_member_entries(
        self,
        member_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        async_req: bool = True,
    ) -> Thread: ...

    @overload
    def get_member_entries(
        self,
        member_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        async_req: bool = False,
    ) -> List[EntradasResumoApiViewModel]: ...

    def get_member_entries(
        self,
        member_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        async_req: bool = False,
    ) -> Union[List[EntradasResumoApiViewModel], Thread]:
        """
        Convenience method to get entries for a specific member.

        Args:
            member_id: ID of the member
            start_date: Optional start date filter
            end_date: Optional end date filter
            async_req: Execute request asynchronously
        """
        return self.get_entries(
            member_id=member_id,
            register_date_start=start_date,
            register_date_end=end_date,
            async_req=async_req,
        )

    @overload
    def get_entry_by_id(self, entry_id: int, async_req: bool = True) -> Thread: ...

    @overload
    def get_entry_by_id(
        self, entry_id: int, async_req: bool = False
    ) -> Optional[EntradasResumoApiViewModel]: ...

    def get_entry_by_id(
        self, entry_id: int, async_req: bool = False
    ) -> Union[Optional[EntradasResumoApiViewModel], Thread]:
        """
        Get a specific entry by ID.

        Args:
            entry_id: ID of the entry to retrieve
            async_req: Execute request asynchronously
        """
        entries = self.get_entries(entry_id=entry_id, async_req=async_req)
        if isinstance(entries, Thread):
            return entries
        return entries[0] if entries else None
