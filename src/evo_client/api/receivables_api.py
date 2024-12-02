from datetime import datetime
from multiprocessing.pool import AsyncResult
from typing import Any, List, Optional, Union, overload, Literal

from ..core.api_client import ApiClient
from ..models.receivables_api_view_model import ReceivablesApiViewModel
from ..models.receivables_mask_received_view_model import (
    ReceivablesMaskReceivedViewModel,
)
from ..models.revenue_center_api_view_model import RevenueCenterApiViewModel


class ReceivablesApi:
    """Receivables API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1"

    @overload
    def get_receivables(
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
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    @overload
    def get_receivables(
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
        async_req: Literal[False] = False,
    ) -> List[ReceivablesApiViewModel]: ...

    def get_receivables(
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
        async_req: bool = False,
    ) -> Union[List[ReceivablesApiViewModel], AsyncResult[Any]]:
        """
        Get receivables with optional filtering.

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
            async_req: Execute request asynchronously
        """
        params = {
            "registrationDateStart": registration_date_start,
            "registrationDateEnd": registration_date_end,
            "dueDateStart": due_date_start,
            "dueDateEnd": due_date_end,
            "receivingDateStart": receiving_date_start,
            "receivingDateEnd": receiving_date_end,
            "competenceDateStart": competence_date_start,
            "competenceDateEnd": competence_date_end,
            "cancellationDateStart": cancellation_date_start,
            "cancellationDateEnd": cancellation_date_end,
            "chargeDateStart": charge_date_start,
            "chargeDateEnd": charge_date_end,
            "updateDateStart": update_date_start,
            "updateDateEnd": update_date_end,
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
            "invoiceDateStart": invoice_date_start,
            "invoiceDateEnd": invoice_date_end,
            "invoiceCanceledDateStart": invoice_canceled_date_start,
            "invoiceCanceledDateEnd": invoice_canceled_date_end,
            "saleDateStart": sale_date_start,
            "saleDateEnd": sale_date_end,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/receivables",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[ReceivablesApiViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def get_revenue_centers(
        self,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    @overload
    def get_revenue_centers(
        self,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: Literal[False] = False,
    ) -> RevenueCenterApiViewModel: ...

    def get_revenue_centers(
        self,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[RevenueCenterApiViewModel, AsyncResult[Any]]:
        """
        Get revenue centers with pagination.

        Args:
            take: Number of records to return
            skip: Number of records to skip
            async_req: Execute request asynchronously
        """
        params = {
            "take": take,
            "skip": skip,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/revenuecenter",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=RevenueCenterApiViewModel,
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def mark_received(
        self,
        receivables: ReceivablesMaskReceivedViewModel,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    @overload
    def mark_received(
        self,
        receivables: ReceivablesMaskReceivedViewModel,
        async_req: Literal[False] = False,
    ) -> Any: ...

    def mark_received(
        self, receivables: ReceivablesMaskReceivedViewModel, async_req: bool = False
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Mark receivables as received.

        Args:
            receivables: Receivables to mark as received
            async_req: Execute request asynchronously
        """
        return self.api_client.call_api(
            resource_path=f"{self.base_path}/receivables/mark-received",
            method="PUT",
            body=receivables,
            response_type=None,
            auth_settings=["Basic"],
            async_req=async_req,
        )
