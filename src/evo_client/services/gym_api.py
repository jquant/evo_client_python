# /src/evo_client/api/gym_api.py

from __future__ import absolute_import

from datetime import datetime, timedelta
from decimal import Decimal
from multiprocessing.pool import Pool
from typing import Any, Dict, List, Optional

from loguru import logger

from ..models.receivables_api_view_model import ReceivablesApiViewModel
from .data_fetchers import BranchApiClientManager
from .data_fetchers.activity_data_fetcher import ActivityDataFetcher
from .data_fetchers.configuration_data_fetcher import ConfigurationDataFetcher
from .data_fetchers.entries_data_fetcher import EntriesDataFetcher

# Import data fetchers
from .data_fetchers.member_data_fetcher import MemberDataFetcher
from .data_fetchers.membership_data_fetcher import MembershipDataFetcher
from .data_fetchers.prospects_data_fetcher import ProspectsDataFetcher
from .data_fetchers.receivables_data_fetcher import ReceivablesDataFetcher
from .data_fetchers.sales_data_fetcher import SalesDataFetcher
from .data_fetchers.service_data_fetcher import ServiceDataFetcher
from .gym_knowledge_base.gym_kb_data_fetcher import GymKnowledgeBaseService

# Models from gym_model
try:
    from ..models.gym_model import OverdueMember
except ImportError as e:
    logger.error(f"Error importing gym_model: {str(e)}")
    raise ValueError(f"Error importing gym_model: {str(e)}")


class GymApi:
    """Gym API client for EVO API."""

    _pool: Pool
    branch_ids: List[int]

    def __init__(
        self,
        client_manager: BranchApiClientManager,
    ):
        """Initialize the gym API.

        Args:
            client_manager: The client manager instance
        """
        # Initialize data fetchers with branch awareness
        self.configuration_data_fetcher = ConfigurationDataFetcher(
            client_manager=client_manager
        )
        self.member_data_fetcher = MemberDataFetcher(
            client_manager=client_manager,
        )
        self.receivables_data_fetcher = ReceivablesDataFetcher(
            client_manager=client_manager,
        )
        self.entries_data_fetcher = EntriesDataFetcher(
            client_manager=client_manager,
        )
        self.prospects_data_fetcher = ProspectsDataFetcher(
            client_manager=client_manager,
        )
        self.activity_data_fetcher = ActivityDataFetcher(
            client_manager=client_manager,
        )
        self.service_data_fetcher = ServiceDataFetcher(
            client_manager=client_manager,
        )
        self.membership_data_fetcher = MembershipDataFetcher(
            client_manager=client_manager,
        )
        self.sales_data_fetcher = SalesDataFetcher(
            client_manager=client_manager,
        )
        self.knowledge_base_fetcher = GymKnowledgeBaseService(
            client_manager=client_manager,
        )

    def __del__(self):
        """Clean up resources."""
        if hasattr(self, "_pool"):
            self._pool.close()
            self._pool.join()

    def get_overdue_members(
        self, min_days_overdue: int = 1, branch_ids: Optional[List[int]] = None
    ) -> List[OverdueMember]:
        """Get members with overdue payments.

        Args:
            min_days_overdue: Minimum days overdue (default: 1)
            branch_ids: Optional list of branch IDs to filter by

        Returns:
            List of overdue members
        """
        # Calculate the date range for overdue receivables
        current_date = datetime.now()
        from_date = current_date - timedelta(days=min_days_overdue)

        # Get overdue receivables using the data fetcher
        raw_receivables = self.receivables_data_fetcher.fetch_receivables(
            due_date_start=from_date,
            due_date_end=current_date,
            payment_types="0",  # em atraso
            account_status="1",  # 1 para cliente ativo (opened) e 4 para cliente inativo catraca bloqueada (overdue)
        )

        # Process the receivables
        receivables: List[ReceivablesApiViewModel] = []

        def process_receivable(item: Any) -> None:
            if isinstance(item, ReceivablesApiViewModel):
                # Filter by branch if needed
                if not branch_ids or (item.id_branch_member in branch_ids):
                    receivables.append(item)
            elif isinstance(item, list):
                for sub_item in item:
                    process_receivable(sub_item)

        # Handle the raw response which could be a single object, a list, or nested lists
        if isinstance(raw_receivables, list):
            for item in raw_receivables:
                process_receivable(item)
        else:
            process_receivable(raw_receivables)

        # Group the receivables by member
        return self._group_overdue_receivables(receivables)

    def _group_overdue_receivables(
        self, receivables: List[ReceivablesApiViewModel]
    ) -> List[OverdueMember]:
        """Group overdue receivables by member and branch."""
        member_map: Dict[tuple[int, Optional[int]], OverdueMember] = {}

        # Keep track of processed receivable IDs to avoid duplicates
        processed_receivables = set()

        for receivable in receivables:
            # Skip if we've already processed this receivable
            if receivable.id_receivable in processed_receivables:
                continue

            if not receivable.id_member_payer:
                logger.warning(
                    f"Receivable {receivable.id_receivable} has no member payer"
                )
                continue

            key = (receivable.id_member_payer, receivable.id_branch_member)
            processed_receivables.add(receivable.id_receivable)

            if key not in member_map:
                member_map[key] = OverdueMember(
                    id=receivable.id_receivable or 0,
                    name=receivable.payer_name or "Unknown",
                    member_id=receivable.id_member_payer,
                    total_overdue=Decimal("0.00"),
                    overdue_since=receivable.due_date or datetime.now(),
                    overdue_receivables=[],
                    branch_id=receivable.id_branch_member,
                    last_payment_date=None,
                )

            member = member_map[key]
            amount = Decimal(str(receivable.ammount or 0))
            amount_paid = Decimal(str(receivable.ammount_paid or 0))
            member.total_overdue += amount - amount_paid
            member.overdue_receivables.append(receivable)

            # Update overdue_since if this receivable is older
            if receivable.due_date and receivable.due_date < member.overdue_since:
                member.overdue_since = receivable.due_date

        return list(member_map.values())
