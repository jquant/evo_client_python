from typing import List, Optional, Dict
from datetime import datetime

from evo_client.api.sales_api import SalesApi
from evo_client.core.api_client import ApiClient
from evo_client.models.sales_view_model import SalesViewModel
from evo_client.utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher


class SalesDataFetcher(BaseDataFetcher):
    """Handles fetching and processing sales-related data."""
    
    def __init__(self, sales_api: SalesApi, branch_api_clients: Optional[Dict[str, ApiClient]] = None):
        super().__init__(sales_api, branch_api_clients)
    
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
        """Fetch sales with various filters."""
        return paginated_api_call(
            api_func=self.api.get_sales,
            parallel_units=self.branch_ids,
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
