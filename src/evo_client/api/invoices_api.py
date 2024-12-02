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
from typing import Any, List, Literal, Optional, Union, overload

from evo_client.core.api_client import ApiClient

from ..models.enotas_retorno import EnotasRetorno, InvoiceStatus, InvoiceType

# python 2 and python 3 compatibility library


class InvoicesApi:
    """Invoices API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/invoices"

    @overload
    def get_invoices(
        self,
        issue_date_start: Optional[datetime] = None,
        issue_date_end: Optional[datetime] = None,
        competency_date_start: Optional[datetime] = None,
        competency_date_end: Optional[datetime] = None,
        send_date_start: Optional[datetime] = None,
        send_date_end: Optional[datetime] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        member_id: Optional[int] = None,
        status_invoice: Optional[List[InvoiceStatus]] = None,
        types_invoice: Optional[List[InvoiceType]] = None,
        async_req: Literal[False] = False,
    ) -> EnotasRetorno: ...

    @overload
    def get_invoices(
        self,
        issue_date_start: Optional[datetime] = None,
        issue_date_end: Optional[datetime] = None,
        competency_date_start: Optional[datetime] = None,
        competency_date_end: Optional[datetime] = None,
        send_date_start: Optional[datetime] = None,
        send_date_end: Optional[datetime] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        member_id: Optional[int] = None,
        status_invoice: Optional[List[InvoiceStatus]] = None,
        types_invoice: Optional[List[InvoiceType]] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    def get_invoices(
        self,
        issue_date_start: Optional[datetime] = None,
        issue_date_end: Optional[datetime] = None,
        competency_date_start: Optional[datetime] = None,
        competency_date_end: Optional[datetime] = None,
        send_date_start: Optional[datetime] = None,
        send_date_end: Optional[datetime] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        member_id: Optional[int] = None,
        status_invoice: Optional[List[InvoiceStatus]] = None,
        types_invoice: Optional[List[InvoiceType]] = None,
        async_req: bool = False,
    ) -> Union[EnotasRetorno, AsyncResult[Any]]:
        """
        Get invoices by date and other filters.

        Args:
            issue_date_start: Filter by invoice issuance start date
            issue_date_end: Filter by invoice issuance end date
            competency_date_start: Filter by competency start date
            competency_date_end: Filter by competency end date
            send_date_start: Filter by sending start date
            send_date_end: Filter by sending end date
            take: Number of records to return (max 250)
            skip: Number of records to skip
            member_id: Filter by member ID
            status_invoice: Filter by invoice status
            types_invoice: Filter by invoice types
            async_req: Execute request asynchronously

        Returns:
            Invoice response or AsyncResult[Any] if async

        Raises:
            ValueError: If take > 250
        """
        if take and take > 250:
            raise ValueError("Maximum number of records to return is 250")

        # Convert enum lists to comma-separated strings
        status_str = (
            ",".join(str(s.value) for s in status_invoice) if status_invoice else None
        )
        types_str = (
            ",".join(str(t.value) for t in types_invoice) if types_invoice else None
        )

        params = {
            "issueDateStart": issue_date_start,
            "issueDateEnd": issue_date_end,
            "competencyDateStart": competency_date_start,
            "competencyDateEnd": competency_date_end,
            "sendDateStart": send_date_start,
            "sendDateEnd": send_date_end,
            "take": take,
            "skip": skip,
            "idMember": member_id,
            "statusInvoice": status_str,
            "typesInvoice": types_str,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/get-invoices",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=EnotasRetorno,
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )
