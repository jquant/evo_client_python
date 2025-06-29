"""Clean synchronous Invoices API."""

from datetime import datetime
from typing import List, Optional, cast

from ...models.enotas_retorno import EnotasRetorno, InvoiceStatus, InvoiceType
from .base import SyncBaseApi


class SyncInvoicesApi(SyncBaseApi):
    """Clean synchronous Invoices API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/invoices"

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
    ) -> EnotasRetorno:
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
            status_invoice: Filter by invoice status list
            types_invoice: Filter by invoice types list

        Returns:
            Invoice response with matching invoices

        Raises:
            ValueError: If take > 250

        Example:
            >>> with SyncInvoicesApi() as api:
            ...     invoices = api.get_invoices(
            ...         issue_date_start=datetime(2024, 1, 1),
            ...         issue_date_end=datetime(2024, 12, 31),
            ...         member_id=123,
            ...         take=50
            ...     )
            ...     print(f"Found {len(invoices.data)} invoices")
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

        result = self.api_client.call_api(
            resource_path=f"{self.base_path}/get-invoices",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=EnotasRetorno,
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return cast(EnotasRetorno, result)
