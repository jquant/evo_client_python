from datetime import datetime
from multiprocessing.pool import AsyncResult
from typing import Any, List, Literal, Optional, Union, overload

from ..core.api_client import ApiClient
from ..models.new_sale_view_model import NewSaleResponse, NewSaleViewModel
from ..models.sales_items_view_model import SalesItemsViewModel
from ..models.sales_view_model import SalesViewModel
from .base import BaseApi


class SalesApi(BaseApi):
    """Sales API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        super().__init__(api_client)
        self.base_path = "/api/v1/sales"

    @overload
    def get_sale_by_id(
        self, sale_id: int, async_req: Literal[False] = False
    ) -> SalesViewModel:
        ...

    @overload
    def get_sale_by_id(
        self, sale_id: int, async_req: Literal[True] = True
    ) -> AsyncResult[Any]:
        ...

    def get_sale_by_id(
        self, sale_id: int, async_req: bool = False
    ) -> Union[SalesViewModel, AsyncResult[Any]]:
        """Get sale by ID."""
        if not sale_id:
            raise ValueError("sale_id is required")

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/{sale_id}",
            method="GET",
            response_type=SalesViewModel,
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def create_sale(
        self, body: Optional[NewSaleViewModel] = None, async_req: Literal[False] = False
    ) -> NewSaleResponse:
        ...

    @overload
    def create_sale(
        self, body: Optional[NewSaleViewModel] = None, async_req: Literal[True] = True
    ) -> AsyncResult[Any]:
        ...

    def create_sale(
        self, body: Optional[NewSaleViewModel] = None, async_req: bool = False
    ) -> Union[NewSaleResponse, AsyncResult[Any]]:
        """
        Create a new sale.

        Payment types:
        - 1: Credit Card
        - 2: Boleto
        - 3: Sale Credits
        - 4: Transfer
        - 5: ValorZerado
        - 6: LinkCheckout
        - 7: Pix
        """
        return self.api_client.call_api(
            resource_path=self.base_path,
            method="POST",
            body=body.model_dump(exclude_unset=True) if body else None,
            response_type=NewSaleResponse,
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
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
        async_req: Literal[False] = False,
    ) -> List[SalesViewModel]:
        ...

    @overload
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
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]:
        ...

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
        async_req: bool = False,
    ) -> Union[List[SalesViewModel], AsyncResult[Any]]:
        """
        Get sales with various filtering options.

        Args:
            member_id: Filter by member ID
            date_sale_start: Filter sales starting from date
            date_sale_end: Filter sales until date
            removal_date_start: Filter removed sales from date
            removal_date_end: Filter removed sales until date
            receivables_registration_date_start: Filter receivables from date
            receivables_registration_date_end: Filter receivables until date
            show_receivables: Show sale receivables details
            take: Number of records to return (max 100, default 25)
            skip: Number of records to skip
            only_membership: Return only membership sales
            at_least_monthly: Filter out memberships less than 30 days
            fl_swimming: Filter by swimming flag
            show_only_active_memberships: Show only active memberships
            show_allow_locker: Show sales with locker access
            only_total_pass: Show only total pass sales
        """
        params = {
            "idMember": member_id,
            "dateSaleStart": date_sale_start,
            "dateSaleEnd": date_sale_end,
            "removalDateStart": removal_date_start,
            "removalDateEnd": removal_date_end,
            "receivablesRegistrationDateStart": receivables_registration_date_start,
            "receivablesRegistrationDateEnd": receivables_registration_date_end,
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

        return self.api_client.call_api(
            resource_path="/api/v2/sales",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[SalesViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def get_sales_items(
        self, branch_id: Optional[int] = None, async_req: Literal[False] = False
    ) -> List[SalesItemsViewModel]:
        ...

    @overload
    def get_sales_items(
        self, branch_id: Optional[int] = None, async_req: Literal[True] = True
    ) -> AsyncResult[Any]:
        ...

    def get_sales_items(
        self, branch_id: Optional[int] = None, async_req: bool = False
    ) -> Union[List[SalesItemsViewModel], AsyncResult[Any]]:
        """Get items available for sale."""
        params = {"idBranch": branch_id} if branch_id else {}

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/sales-items",
            method="GET",
            query_params=params,
            response_type=List[SalesItemsViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def get_sale_by_session_id(
        self,
        session_id: str,
        date: Optional[datetime] = None,
        async_req: Literal[False] = False,
    ) -> int:
        ...

    @overload
    def get_sale_by_session_id(
        self,
        session_id: str,
        date: Optional[datetime] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]:
        ...

    def get_sale_by_session_id(
        self, session_id: str, date: Optional[datetime] = None, async_req: bool = False
    ) -> Union[int, AsyncResult[Any]]:
        """Get sale ID by session ID."""
        params = {"sessionId": session_id, "date": date}

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/by-session-id",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=int,
            auth_settings=["Basic"],
            async_req=async_req,
        )
