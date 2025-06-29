"""Clean asynchronous Receivables API."""

from datetime import datetime
from typing import Any, List, Optional, cast

from ...models.receivables_api_view_model import ReceivablesApiViewModel
from ...models.receivables_mask_received_view_model import (
    ReceivablesMaskReceivedViewModel,
)
from ...models.revenue_center_api_view_model import RevenueCenterApiViewModel
from .base import AsyncBaseApi


class AsyncReceivablesApi(AsyncBaseApi):
    """Clean asynchronous Receivables API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1"

    async def get_receivables(
        self,
        registration_date_start: Optional[datetime] = None,
        registration_date_end: Optional[datetime] = None,
        due_date_start: Optional[datetime] = None,
        due_date_end: Optional[datetime] = None,
        receiving_date_start: Optional[datetime] = None,
        receiving_date_end: Optional[datetime] = None,
        competence_date_start: Optional[datetime] = None,
        competence_date_end: Optional[datetime] = None,
        cancellation_date_start: Optional[datetime] = None,
        cancellation_date_end: Optional[datetime] = None,
        charge_date_start: Optional[datetime] = None,
        charge_date_end: Optional[datetime] = None,
        update_date_start: Optional[datetime] = None,
        update_date_end: Optional[datetime] = None,
        description: Optional[str] = None,
        amount_start: Optional[float] = None,
        amount_end: Optional[float] = None,
        payment_types: Optional[str] = None,
        account_status: Optional[str] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        member_id: Optional[int] = None,
        sale_id: Optional[int] = None,
        receivable_id: Optional[int] = None,
        invoice_date_start: Optional[datetime] = None,
        invoice_date_end: Optional[datetime] = None,
        invoice_canceled_date_start: Optional[datetime] = None,
        invoice_canceled_date_end: Optional[datetime] = None,
        sale_date_start: Optional[datetime] = None,
        sale_date_end: Optional[datetime] = None,
    ) -> List[ReceivablesApiViewModel]:
        """
        Get receivables with comprehensive filtering options.

        Args:
            registration_date_start: Filter by registration start date (yyyy-mm-dd)
            registration_date_end: Filter by registration end date (yyyy-mm-dd)
            due_date_start: Filter by due date start (yyyy-mm-dd)
            due_date_end: Filter by due date end (yyyy-mm-dd)
            receiving_date_start: Filter by receiving date start (yyyy-mm-dd)
            receiving_date_end: Filter by receiving date end (yyyy-mm-dd)
            competence_date_start: Filter by competence start date (yyyy-mm-dd)
            competence_date_end: Filter by competence end date (yyyy-mm-dd)
            cancellation_date_start: Filter by cancellation start date (yyyy-mm-dd)
            cancellation_date_end: Filter by cancellation end date (yyyy-mm-dd)
            charge_date_start: Filter by charge start date (yyyy-mm-dd)
            charge_date_end: Filter by charge end date (yyyy-mm-dd)
            update_date_start: Filter by update start date (yyyy-mm-dd)
            update_date_end: Filter by update end date (yyyy-mm-dd)
            description: Filter by description
            amount_start: Filter by minimum amount
            amount_end: Filter by maximum amount
            payment_types: Filter by payment types (comma separated). Types:
                1=Money, 2=Credit Card, 3=Debit Card, 4=Check, 5=Boleto Bancário,
                6=PagSeguro, 7=Deposit, 8=Account Debit, 9=Internet, 11=Sale Credits,
                12=On-line Credit Card, 13=Transfer, 18=Pix, 0=Balance Due
            account_status: Filter by status (comma separated). Status:
                1=Opened, 2=Received, 3=Canceled, 4=Overdue
            take: Number of records to return (max 50)
            skip: Number of records to skip
            member_id: Filter by member ID
            sale_id: Filter by sale ID
            receivable_id: Filter by receivable ID
            invoice_date_start: Filter by invoice start date (yyyy-mm-dd)
            invoice_date_end: Filter by invoice end date (yyyy-mm-dd)
            invoice_canceled_date_start: Filter by canceled invoice start date (yyyy-mm-dd)
            invoice_canceled_date_end: Filter by canceled invoice end date (yyyy-mm-dd)
            sale_date_start: Filter by sale start date (yyyy-mm-dd)
            sale_date_end: Filter by sale end date (yyyy-mm-dd)

        Returns:
            List of receivables matching the criteria

        Example:
            >>> async with AsyncReceivablesApi() as api:
            ...     receivables = await api.get_receivables(
            ...         due_date_start=datetime(2024, 1, 1),
            ...         due_date_end=datetime(2024, 12, 31),
            ...         account_status="4",  # Overdue
            ...         take=25
            ...     )
            ...     for receivable in receivables:
            ...         print(f"ID: {receivable.id_receivable} - Amount: ${receivable.ammount}")
        """
        params = {
            "registrationDateStart": (
                registration_date_start.isoformat() if registration_date_start else None
            ),
            "registrationDateEnd": (
                registration_date_end.isoformat() if registration_date_end else None
            ),
            "dueDateStart": due_date_start.isoformat() if due_date_start else None,
            "dueDateEnd": due_date_end.isoformat() if due_date_end else None,
            "receivingDateStart": (
                receiving_date_start.isoformat() if receiving_date_start else None
            ),
            "receivingDateEnd": (
                receiving_date_end.isoformat() if receiving_date_end else None
            ),
            "competenceDateStart": (
                competence_date_start.isoformat() if competence_date_start else None
            ),
            "competenceDateEnd": (
                competence_date_end.isoformat() if competence_date_end else None
            ),
            "cancellationDateStart": (
                cancellation_date_start.isoformat() if cancellation_date_start else None
            ),
            "cancellationDateEnd": (
                cancellation_date_end.isoformat() if cancellation_date_end else None
            ),
            "chargeDateStart": (
                charge_date_start.isoformat() if charge_date_start else None
            ),
            "chargeDateEnd": charge_date_end.isoformat() if charge_date_end else None,
            "updateDateStart": (
                update_date_start.isoformat() if update_date_start else None
            ),
            "updateDateEnd": update_date_end.isoformat() if update_date_end else None,
            "description": description,
            "ammountStart": amount_start,
            "ammountEnd": amount_end,
            "paymentTypes": payment_types,
            "accountStatus": account_status,
            "take": take,
            "skip": skip,
            "memberId": member_id,
            "idSale": sale_id,
            "idReceivable": receivable_id,
            "invoiceDateStart": (
                invoice_date_start.isoformat() if invoice_date_start else None
            ),
            "invoiceDateEnd": (
                invoice_date_end.isoformat() if invoice_date_end else None
            ),
            "invoiceCanceledDateStart": (
                invoice_canceled_date_start.isoformat()
                if invoice_canceled_date_start
                else None
            ),
            "invoiceCanceledDateEnd": (
                invoice_canceled_date_end.isoformat()
                if invoice_canceled_date_end
                else None
            ),
            "saleDateStart": sale_date_start.isoformat() if sale_date_start else None,
            "saleDateEnd": sale_date_end.isoformat() if sale_date_end else None,
        }

        result = await self.api_client.call_api(
            resource_path=f"{self.base_path}/receivables",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[ReceivablesApiViewModel],
            auth_settings=["Basic"],
        )
        return cast(List[ReceivablesApiViewModel], result)

    async def get_revenue_centers(
        self,
        take: Optional[int] = None,
        skip: Optional[int] = None,
    ) -> RevenueCenterApiViewModel:
        """
        Get revenue centers.

        Args:
            take: Number of records to return
            skip: Number of records to skip

        Returns:
            Revenue center information

        Example:
            >>> async with AsyncReceivablesApi() as api:
            ...     revenue_centers = await api.get_revenue_centers(take=10)
            ...     print(f"Centers: {revenue_centers}")
        """
        params = {
            "take": take,
            "skip": skip,
        }

        result = await self.api_client.call_api(
            resource_path=f"{self.base_path}/revenue-centers",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=RevenueCenterApiViewModel,
            auth_settings=["Basic"],
        )
        return cast(RevenueCenterApiViewModel, result)

    async def mark_received(self, receivables: ReceivablesMaskReceivedViewModel) -> Any:
        """
        Mark receivables as received.

        Args:
            receivables: Receivables data to mark as received

        Returns:
            Operation result

        Example:
            >>> async with AsyncReceivablesApi() as api:
            ...     receivables_data = ReceivablesMaskReceivedViewModel(
            ...         receivable_ids=[123, 456],
            ...         received_date=datetime.now()
            ...     )
            ...     result = await api.mark_received(receivables_data)
        """
        return await self.api_client.call_api(
            resource_path=f"{self.base_path}/receivables/received",
            method="PUT",
            body=receivables.model_dump(exclude_unset=True, by_alias=True),
            auth_settings=["Basic"],
        )
