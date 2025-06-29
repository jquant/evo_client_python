"""Clean synchronous Payables API."""

from datetime import datetime
from typing import Optional, cast

from ...models.cost_center_api_view_model import CostCenterApiViewModel
from ...models.payables_api_view_model import PayablesApiViewModel
from .base import SyncBaseApi


class SyncPayablesApi(SyncBaseApi):
    """Clean synchronous Payables API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1"

    def get_cost_centers(
        self,
        take: Optional[int] = None,
        skip: Optional[int] = None,
    ) -> CostCenterApiViewModel:
        """
        Get cost centers with pagination.

        Args:
            take: Number of records to return
            skip: Number of records to skip

        Returns:
            Cost center information

        Example:
            >>> with SyncPayablesApi() as api:
            ...     cost_centers = api.get_cost_centers(take=10)
            ...     print(f"Cost centers: {cost_centers}")
        """
        params = {
            "take": take,
            "skip": skip,
        }

        result = self.api_client.call_api(
            resource_path=f"{self.base_path}/costcenter",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=CostCenterApiViewModel,
            auth_settings=["Basic"],
        )
        return cast(CostCenterApiViewModel, result)

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
    ) -> PayablesApiViewModel:
        """
        Get payables with comprehensive filtering options.

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

        Returns:
            Payables matching the criteria

        Example:
            >>> with SyncPayablesApi() as api:
            ...     payables = api.get_payables(
            ...         due_date_start=datetime(2024, 1, 1),
            ...         due_date_end=datetime(2024, 12, 31),
            ...         account_status="1",  # Opened
            ...         take=20
            ...     )
            ...     print(f"Found {len(payables.list)} payables")
        """
        params = {
            "description": description,
            "dateInputStart": (
                date_input_start.isoformat() if date_input_start else None
            ),
            "dateInputEnd": date_input_end.isoformat() if date_input_end else None,
            "dueDateStart": due_date_start.isoformat() if due_date_start else None,
            "dueDateEnd": due_date_end.isoformat() if due_date_end else None,
            "datePaymentStart": (
                date_payment_start.isoformat() if date_payment_start else None
            ),
            "datePaymentEnd": (
                date_payment_end.isoformat() if date_payment_end else None
            ),
            "competenceStart": (
                competence_start.isoformat() if competence_start else None
            ),
            "competenceEnd": competence_end.isoformat() if competence_end else None,
            "bankAccount": bank_account,
            "amountStart": amount_start,
            "amountEnd": amount_end,
            "accountStatus": account_status,
            "take": take,
            "skip": skip,
        }

        result = self.api_client.call_api(
            resource_path=f"{self.base_path}/payables",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=PayablesApiViewModel,
            auth_settings=["Basic"],
        )
        return cast(PayablesApiViewModel, result)
