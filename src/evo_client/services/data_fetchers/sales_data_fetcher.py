from datetime import datetime
from typing import List, Optional

from loguru import logger

from ...models.sales_view_model import SalesViewModel
from ...sync.api.sales_api import SyncSalesApi
from ...utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher


class SalesDataFetcher(BaseDataFetcher):
    """Handles fetching and processing sales-related data."""

    def fetch_sales(
        self,
        member_id: Optional[int] = None,
        date_sale_start: Optional[datetime] = None,
        date_sale_end: Optional[datetime] = None,
        removal_date_start: Optional[datetime] = None,
        removal_date_end: Optional[datetime] = None,
        receivables_registration_date_start: Optional[datetime] = None,
        receivables_registration_date_end: Optional[datetime] = None,
        show_receivables: Optional[bool] = None,
        only_membership: Optional[bool] = None,
        at_least_monthly: Optional[bool] = None,
        fl_swimming: Optional[bool] = None,
        show_only_active_memberships: Optional[bool] = None,
        show_allow_locker: Optional[bool] = None,
        only_total_pass: Optional[bool] = None,
    ) -> List[SalesViewModel]:
        """Fetch sales with various filters.

        Args:
            member_id: Filter by member ID
            date_sale_start: Filter by sale start date
            date_sale_end: Filter by sale end date
            removal_date_start: Filter by removal start date
            removal_date_end: Filter by removal end date
            receivables_registration_date_start: Filter by receivables registration start date
            receivables_registration_date_end: Filter by receivables registration end date
            show_receivables: Include receivables in response
            only_membership: Filter for membership sales only
            at_least_monthly: Filter for monthly or longer memberships
            fl_swimming: Filter for swimming-related sales
            show_only_active_memberships: Filter for active memberships only
            show_allow_locker: Filter for sales with locker access
            only_total_pass: Filter for total pass sales only

        Returns:
            List[SalesViewModel]: List of sales matching the filters
        """
        try:
            result = []
            for branch_id in self.get_available_branch_ids():
                branch_api = SyncSalesApi(api_client=self.get_branch_api(branch_id))
                if branch_api:
                    result.extend(
                        paginated_api_call(
                            api_func=branch_api.get_sales,
                            branch_id_logging=str(branch_id),
                            member_id=member_id,
                            date_sale_start=date_sale_start,
                            date_sale_end=date_sale_end,
                            removal_date_start=removal_date_start,
                            removal_date_end=removal_date_end,
                            receivables_registration_date_start=receivables_registration_date_start,
                            receivables_registration_date_end=receivables_registration_date_end,
                            show_receivables=show_receivables,
                            only_membership=only_membership,
                            at_least_monthly=at_least_monthly,
                            fl_swimming=fl_swimming,
                            show_only_active_memberships=show_only_active_memberships,
                            show_allow_locker=show_allow_locker,
                            only_total_pass=only_total_pass,
                        )
                    )

            return result or []

        except Exception as e:
            logger.error(f"Error fetching sales: {str(e)}")
            raise ValueError(f"Error fetching sales: {str(e)}")
