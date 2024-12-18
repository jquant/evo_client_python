from typing import List, Optional, Dict
from datetime import datetime

from evo_client.api.receivables_api import ReceivablesApi
from evo_client.core.api_client import ApiClient
from evo_client.models.receivables_api_view_model import ReceivablesApiViewModel
from evo_client.utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher


class ReceivablesDataFetcher(BaseDataFetcher):
    """Handles fetching and processing receivables-related data."""
    
    def __init__(self, receivables_api: ReceivablesApi, branch_api_clients: Optional[Dict[str, ApiClient]] = None):
        super().__init__(receivables_api, branch_api_clients)
    
    def fetch_receivables(
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
        invoice_date_start: Optional[datetime] = None,
        invoice_date_end: Optional[datetime] = None,
        invoice_canceled_date_start: Optional[datetime] = None,
        invoice_canceled_date_end: Optional[datetime] = None,
        sale_date_start: Optional[datetime] = None,
        sale_date_end: Optional[datetime] = None,
        description: Optional[str] = None,
        amount_start: Optional[float] = None,
        amount_end: Optional[float] = None,
        payment_types: Optional[str] = None,
        account_status: Optional[str] = None,
        member_id: Optional[int] = None,
        sale_id: Optional[int] = None,
        receivable_id: Optional[int] = None,
    ) -> List[ReceivablesApiViewModel]:
        """Fetch receivables with various filters."""
        return paginated_api_call(
            api_func=self.api.get_receivables,
            parallel_units=self.branch_ids,
            registration_date_start=registration_date_start,
            registration_date_end=registration_date_end,
            due_date_start=due_date_start,
            due_date_end=due_date_end,
            receiving_date_start=receiving_date_start,
            receiving_date_end=receiving_date_end,
            competence_date_start=competence_date_start,
            competence_date_end=competence_date_end,
            cancellation_date_start=cancellation_date_start,
            cancellation_date_end=cancellation_date_end,
            charge_date_start=charge_date_start,
            charge_date_end=charge_date_end,
            update_date_start=update_date_start,
            update_date_end=update_date_end,
            invoice_date_start=invoice_date_start,
            invoice_date_end=invoice_date_end,
            invoice_canceled_date_start=invoice_canceled_date_start,
            invoice_canceled_date_end=invoice_canceled_date_end,
            sale_date_start=sale_date_start,
            sale_date_end=sale_date_end,
            description=description,
            amount_start=amount_start,
            amount_end=amount_end,
            payment_types=payment_types,
            account_status=account_status,
            member_id=member_id,
            sale_id=sale_id,
            receivable_id=receivable_id,
        )
