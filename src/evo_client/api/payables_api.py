from datetime import datetime
from multiprocessing.pool import AsyncResult
from typing import Any, Optional, Union, overload

from ..core.api_client import ApiClient
from ..models.cost_center_api_view_model import CostCenterApiViewModel
from ..models.payables_api_view_model import PayablesApiViewModel


class PayablesApi:
    """Payables API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1"

    @overload
    def get_cost_centers(
        self,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = True,
    ) -> AsyncResult[Any]:
        ...

    @overload
    def get_cost_centers(
        self,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = False,
    ) -> CostCenterApiViewModel:
        ...

    def get_cost_centers(
        self,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[CostCenterApiViewModel, AsyncResult[Any]]:
        """
        Get cost centers with pagination.

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
            resource_path=f"{self.base_path}/costcenter",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=CostCenterApiViewModel,
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def get_payables(
        self,
        description: Optional[str] = None,
        date_input_start: Optional[datetime] = None,
        date_input_end: Optional[datetime] = None,
        due_date_start: Optional[datetime] = None,
        due_date_end: Optional[datetime] = None,
        date_payment_start: Optional[datetime] = None,
        date_payment_end: Optional[datetime] = None,
        competence_start: Optional[datetime] = None,
        competence_end: Optional[datetime] = None,
        bank_account: Optional[str] = None,
        amount_start: Optional[float] = None,
        amount_end: Optional[float] = None,
        account_status: Optional[str] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = True,
    ) -> AsyncResult[Any]:
        ...

    @overload
    def get_payables(
        self,
        description: Optional[str] = None,
        date_input_start: Optional[datetime] = None,
        date_input_end: Optional[datetime] = None,
        due_date_start: Optional[datetime] = None,
        due_date_end: Optional[datetime] = None,
        date_payment_start: Optional[datetime] = None,
        date_payment_end: Optional[datetime] = None,
        competence_start: Optional[datetime] = None,
        competence_end: Optional[datetime] = None,
        bank_account: Optional[str] = None,
        amount_start: Optional[float] = None,
        amount_end: Optional[float] = None,
        account_status: Optional[str] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = False,
    ) -> PayablesApiViewModel:
        ...

    def get_payables(
        self,
        description: Optional[str] = None,
        date_input_start: Optional[datetime] = None,
        date_input_end: Optional[datetime] = None,
        due_date_start: Optional[datetime] = None,
        due_date_end: Optional[datetime] = None,
        date_payment_start: Optional[datetime] = None,
        date_payment_end: Optional[datetime] = None,
        competence_start: Optional[datetime] = None,
        competence_end: Optional[datetime] = None,
        bank_account: Optional[str] = None,
        amount_start: Optional[float] = None,
        amount_end: Optional[float] = None,
        account_status: Optional[str] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[PayablesApiViewModel, AsyncResult[Any]]:
        """
        Get payables with optional filtering.

        Args:
            description: Filter by account description
            date_input_start: Filter by input date start (yyyy-mm-dd)
            date_input_end: Filter by input date end (yyyy-mm-dd)
            due_date_start: Filter by due date start (yyyy-mm-dd)
            due_date_end: Filter by due date end (yyyy-mm-dd)
            date_payment_start: Filter by payment date start
            date_payment_end: Filter by payment date end
            competence_start: Filter by competence start date
            competence_end: Filter by competence end date
            bank_account: Filter by bank account IDs (comma separated)
            amount_start: Filter by minimum amount
            amount_end: Filter by maximum amount
            account_status: Filter by status IDs (comma separated). Status: 1=Opened, 2=Paid, 3=Canceled
            take: Number of records to return (max 50)
            skip: Number of records to skip
            async_req: Execute request asynchronously
        """
        params = {
            "description": description,
            "dateInputStart": date_input_start,
            "dateInputEnd": date_input_end,
            "dueDateStart": due_date_start,
            "dueDateEnd": due_date_end,
            "datePaymentStart": date_payment_start,
            "datePaymentEnd": date_payment_end,
            "competenceStart": competence_start,
            "competenceEnd": competence_end,
            "bankAccount": bank_account,
            "amountStart": amount_start,
            "amountEnd": amount_end,
            "accountStatus": account_status,
            "take": take,
            "skip": skip,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/payables",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=PayablesApiViewModel,
            auth_settings=["Basic"],
            async_req=async_req,
        )
