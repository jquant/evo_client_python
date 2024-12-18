from typing import List, Optional, Dict
from datetime import datetime
import logging

from evo_client.api.receivables_api import ReceivablesApi
from evo_client.core.api_client import ApiClient
from evo_client.models.receivables_api_view_model import ReceivablesApiViewModel
from evo_client.utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher

logger = logging.getLogger(__name__)


class ReceivablesDataFetcher(BaseDataFetcher[ReceivablesApi]):
    """Handles fetching and processing receivables-related data."""

    def __init__(
        self,
        receivables_api: ReceivablesApi,
        branch_api_clients: Optional[Dict[str, ApiClient]] = None,
    ):
        """Initialize the receivables data fetcher.

        Args:
            receivables_api: The receivables API instance
            branch_api_clients: Optional dictionary mapping branch IDs to their API clients
        """
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
        default_client: bool = True,
    ) -> List[ReceivablesApiViewModel]:
        """Fetch receivables with various filters.

        Args:
            registration_date_start: Filter by registration start date
            registration_date_end: Filter by registration end date
            due_date_start: Filter by due date start
            due_date_end: Filter by due date end
            receiving_date_start: Filter by receiving date start
            receiving_date_end: Filter by receiving date end
            competence_date_start: Filter by competence date start
            competence_date_end: Filter by competence date end
            cancellation_date_start: Filter by cancellation date start
            cancellation_date_end: Filter by cancellation date end
            charge_date_start: Filter by charge date start
            charge_date_end: Filter by charge date end
            update_date_start: Filter by update date start
            update_date_end: Filter by update date end
            invoice_date_start: Filter by invoice date start
            invoice_date_end: Filter by invoice date end
            invoice_canceled_date_start: Filter by invoice cancellation date start
            invoice_canceled_date_end: Filter by invoice cancellation date end
            sale_date_start: Filter by sale date start
            sale_date_end: Filter by sale date end
            description: Filter by description
            amount_start: Filter by minimum amount
            amount_end: Filter by maximum amount
            payment_types: Filter by payment types
            account_status: Filter by account status
            member_id: Filter by member ID
            sale_id: Filter by sale ID
            receivable_id: Filter by receivable ID
            default_client: If True, fetch data from all branches
        Returns:
            List[ReceivablesApiViewModel]: List of receivables matching the filters
        """
        try:
            if default_client:
                result = paginated_api_call(
                    api_func=self.api.get_receivables,
                    unit_id="defaut",
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
            else:
                result = []
                for branch_id in self.get_available_branch_ids():
                    branch_api = self.get_branch_api(branch_id, ReceivablesApi)
                    if branch_api:
                        result.extend(
                            paginated_api_call(
                                api_func=branch_api.get_receivables,
                                unit_id=str(branch_id),
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
                        )

            return result or []

        except Exception as e:
            logger.error(f"Error fetching receivables: {str(e)}")
            raise ValueError(f"Error fetching receivables: {str(e)}")
