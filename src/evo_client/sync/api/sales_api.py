"""Clean synchronous Sales API."""

from datetime import datetime
from typing import Any, List, Optional, cast

from ...models.new_sale_view_model import NewSaleResponse, NewSaleViewModel
from ...models.sales_items_view_model import SalesItemsViewModel
from ...models.sales_view_model import SalesViewModel
from .base import SyncBaseApi


class SyncSalesApi(SyncBaseApi):
    """Clean synchronous Sales API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path_v1 = "/api/v1/sales"
        self.base_path_v2 = "/api/v2/sales"

    def get_sale_by_id(self, sale_id: int) -> SalesViewModel:
        """
        Get sale by ID.

        Args:
            sale_id: The ID of the sale to retrieve

        Returns:
            Sale details

        Raises:
            ValueError: If sale_id is not provided

        Example:
            >>> with SyncSalesApi() as api:
            ...     sale = api.get_sale_by_id(12345)
            ...     print(f"Sale #{sale.id} - Total: ${sale.total}")
        """
        if not sale_id:
            raise ValueError("sale_id is required")

        result = self.api_client.call_api(
            resource_path=f"{self.base_path_v1}/{sale_id}",
            method="GET",
            response_type=SalesViewModel,
            auth_settings=["Basic"],
        )
        return cast(SalesViewModel, result)

    def create_sale(self, body: Optional[NewSaleViewModel] = None) -> NewSaleResponse:
        """
        Create a new sale.

        Args:
            body: Sale data to create

        Returns:
            Created sale response

        Note:
            Payment types:
            - 1: Credit Card
            - 2: Boleto
            - 3: Sale Credits
            - 4: Transfer
            - 5: ValorZerado
            - 6: LinkCheckout
            - 7: Pix

        Example:
            >>> with SyncSalesApi() as api:
            ...     sale_data = NewSaleViewModel(member_id=123, items=[...])
            ...     response = api.create_sale(sale_data)
            ...     print(f"Sale created with ID: {response.sale_id}")
        """
        result = self.api_client.call_api(
            resource_path=self.base_path_v1,
            method="POST",
            body=body.model_dump(exclude_unset=True, by_alias=True) if body else None,
            response_type=NewSaleResponse,
            auth_settings=["Basic"],
        )
        return cast(NewSaleResponse, result)

    def get_sales(
        self,
        member_id: Optional[int] = None,
        date_sale_start: Optional[datetime] = None,
        date_sale_end: Optional[datetime] = None,
        removal_date_start: Optional[datetime] = None,
        removal_date_end: Optional[datetime] = None,
        receivables_registration_date_start: Optional[datetime] = None,
        receivables_registration_date_end: Optional[datetime] = None,
        show_receivables: Optional[bool] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        only_membership: Optional[bool] = None,
        at_least_monthly: Optional[bool] = None,
        fl_swimming: Optional[bool] = None,
        show_only_active_memberships: Optional[bool] = None,
        show_allow_locker: Optional[bool] = None,
        only_total_pass: Optional[bool] = None,
    ) -> List[SalesViewModel]:
        """
        Get sales with optional filtering.

        Args:
            member_id: Filter by member ID
            date_sale_start: Start date for sale registration
            date_sale_end: End date for sale registration
            removal_date_start: Start date for sale removal
            removal_date_end: End date for sale removal
            receivables_registration_date_start: Start date for receivables registration
            receivables_registration_date_end: End date for receivables registration
            show_receivables: Show sale receivables and sale value without credit value
            take: Number of records to return (max 100, default 25)
            skip: Number of records to skip
            only_membership: Return only sales with membership
            at_least_monthly: Remove memberships less than 30 days old
            fl_swimming: Filter memberships by swimming flag
            show_only_active_memberships: Show only active memberships
            show_allow_locker: Allow locker display
            only_total_pass: Show only total pass

        Returns:
            List of sales matching the criteria

        Example:
            >>> with SyncSalesApi() as api:
            ...     sales = api.get_sales(member_id=123, take=10)
            ...     for sale in sales:
            ...         print(f"Sale #{sale.id} - ${sale.total}")
        """
        params = {
            "idMember": member_id,
            "dateSaleStart": date_sale_start.isoformat() if date_sale_start else None,
            "dateSaleEnd": date_sale_end.isoformat() if date_sale_end else None,
            "removalDateStart": (
                removal_date_start.isoformat() if removal_date_start else None
            ),
            "removalDateEnd": (
                removal_date_end.isoformat() if removal_date_end else None
            ),
            "receivablesRegistrationDateStart": (
                receivables_registration_date_start.isoformat()
                if receivables_registration_date_start
                else None
            ),
            "receivablesRegistrationDateEnd": (
                receivables_registration_date_end.isoformat()
                if receivables_registration_date_end
                else None
            ),
            "showReceivables": show_receivables,
            "take": take,
            "skip": skip,
            "onlyMembership": only_membership,
            "atLeastMonthly": at_least_monthly,
            "flSwimming": fl_swimming,
            "showOnlyActiveMemberships": show_only_active_memberships,
            "showAllowLocker": show_allow_locker,
            "onlyTotalPass": only_total_pass,
        }

        result = self.api_client.call_api(
            resource_path=self.base_path_v2,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[SalesViewModel],
            auth_settings=["Basic"],
        )
        return cast(List[SalesViewModel], result)

    def get_sales_items(
        self, branch_id: Optional[int] = None
    ) -> List[SalesItemsViewModel]:
        """
        Get available sales items.

        Args:
            branch_id: Optional branch ID filter

        Returns:
            List of available sales items

        Example:
            >>> with SyncSalesApi() as api:
            ...     items = api.get_sales_items(branch_id=1)
            ...     for item in items:
            ...         print(f"{item.name} - ${item.price}")
        """
        params = {}
        if branch_id is not None:
            params["idBranch"] = branch_id

        result = self.api_client.call_api(
            resource_path=f"{self.base_path_v1}/sales-items",
            method="GET",
            query_params=params if params else None,
            response_type=List[SalesItemsViewModel],
            auth_settings=["Basic"],
        )
        return cast(List[SalesItemsViewModel], result)

    def get_sale_by_session_id(
        self, session_id: str, date: Optional[datetime] = None
    ) -> int:
        """
        Get sale ID by session ID.

        Args:
            session_id: The session ID to look up
            date: Optional date filter

        Returns:
            Sale ID

        Example:
            >>> with SyncSalesApi() as api:
            ...     sale_id = api.get_sale_by_session_id("session123")
            ...     print(f"Found sale ID: {sale_id}")
        """
        params = {"sessionId": session_id}
        if date:
            params["date"] = date.isoformat()

        result = self.api_client.call_api(
            resource_path=f"{self.base_path_v1}/by-session-id",
            method="GET",
            query_params=params,
            response_type=None,  # Returns int directly
            auth_settings=["Basic"],
        )
        return cast(int, result)
