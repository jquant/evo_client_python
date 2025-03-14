from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Union

from loguru import logger

from ...models.gym_model import GymOperatingData
from ..data_fetchers import BranchApiClientManager
from ..data_fetchers.entries_data_fetcher import EntriesDataFetcher
from ..data_fetchers.member_data_fetcher import MemberDataFetcher
from ..data_fetchers.membership_data_fetcher import MembershipDataFetcher
from ..data_fetchers.prospects_data_fetcher import ProspectsDataFetcher
from ..data_fetchers.receivables_data_fetcher import ReceivablesDataFetcher
from .operating_data_computer import OperatingDataComputer


class OperatingDataFetcher:
    """Service for fetching and computing operating data metrics."""

    def __init__(self, client_manager: BranchApiClientManager):
        """Initialize the operating data fetcher.

        Args:
            client_manager: The client manager instance
        """
        self.client_manager = client_manager
        self.member_fetcher = MemberDataFetcher(client_manager)
        self.membership_fetcher = MembershipDataFetcher(client_manager)
        self.prospects_fetcher = ProspectsDataFetcher(client_manager)
        self.receivables_fetcher = ReceivablesDataFetcher(client_manager)
        self.entries_fetcher = EntriesDataFetcher(client_manager)
        self.computer = OperatingDataComputer()

    def fetch_operating_data(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        branch_ids: Optional[List[int]] = None,
    ) -> Union[GymOperatingData, List[GymOperatingData]]:
        """Fetch and compute operating data for specified branches.

        Args:
            from_date: Start date for data collection
            to_date: End date for data collection
            branch_ids: Optional list of branch IDs to fetch data for

        Returns:
            Single GymOperatingData object if one branch, or list if multiple branches
        """
        try:
            # Use available branch IDs if none specified
            if branch_ids is None:
                branch_ids = self.client_manager.branch_ids

            # Fetch data for each branch
            branch_data = []
            for branch_id in branch_ids:
                logger.info(f"Fetching operating data for branch {branch_id}")

                # Fetch active members
                active_members = self.member_fetcher.fetch_members(
                    membership_start_date_start=from_date,
                    membership_start_date_end=to_date,
                    status=1,  # Assuming 1 means active
                )

                # Fetch non-renewed members
                non_renewed = self.member_fetcher.fetch_members(
                    membership_cancel_date_start=from_date,
                    membership_cancel_date_end=to_date,
                    status=2,  # Assuming 2 means inactive/cancelled
                )

                # Fetch receivables
                receivables = self.receivables_fetcher.fetch_receivables(
                    due_date_start=from_date, due_date_end=to_date
                )

                # Fetch entries
                entries = self.entries_fetcher.fetch_entries(
                    register_date_start=from_date, register_date_end=to_date
                )

                # Fetch prospects
                prospects = self.prospects_fetcher.fetch_prospects(
                    register_date_start=from_date, register_date_end=to_date
                )

                # Fetch active contracts
                active_contracts = self.membership_fetcher.fetch_memberships(
                    active=True
                )

                # Compute metrics for this branch
                branch_metrics = self.computer.compute_metrics(
                    active_members=active_members,
                    prospects=prospects,
                    active_contracts=active_contracts,
                    non_renewed=non_renewed,
                    receivables=receivables,
                    entries=entries,
                    from_date=from_date,
                    to_date=to_date,
                )

                # Add branch identifier
                branch_metrics.branch_id = str(branch_id)
                branch_data.append(branch_metrics)

            # Return single object if one branch, list if multiple
            if len(branch_data) == 1:
                return branch_data[0]
            return branch_data

        except Exception as e:
            logger.error(f"Error fetching operating data: {str(e)}")
            raise ValueError(f"Error fetching operating data: {str(e)}")

    def aggregate_branch_metrics(
        self, branch_metrics: List[GymOperatingData]
    ) -> GymOperatingData:
        """Aggregate metrics from multiple branches into a single dataset.

        Args:
            branch_metrics: List of branch-specific operating data

        Returns:
            Combined GymOperatingData for all branches
        """
        if not branch_metrics:
            raise ValueError("No branch metrics provided for aggregation")

        # Create base aggregated object
        aggregated = GymOperatingData(
            data_from=branch_metrics[0].data_from, data_to=branch_metrics[0].data_to
        )

        # Aggregate numeric metrics
        aggregated.total_active_members = sum(
            d.total_active_members for d in branch_metrics
        )
        aggregated.total_churned_members = sum(
            d.total_churned_members for d in branch_metrics
        )
        aggregated.total_prospects = sum(d.total_prospects for d in branch_metrics)
        aggregated.mrr = Decimal(sum(d.mrr for d in branch_metrics))
        aggregated.total_paid = Decimal(sum(d.total_paid for d in branch_metrics))
        aggregated.total_pending = Decimal(sum(d.total_pending for d in branch_metrics))
        aggregated.total_overdue = Decimal(sum(d.total_overdue for d in branch_metrics))

        # Calculate weighted average for percentages
        if aggregated.total_active_members > 0:
            aggregated.churn_rate = Decimal(
                sum(d.churn_rate * d.total_active_members for d in branch_metrics)
                / aggregated.total_active_members
            )

            aggregated.multi_unit_member_percentage = Decimal(
                sum(
                    d.multi_unit_member_percentage * d.total_active_members
                    for d in branch_metrics
                )
                / aggregated.total_active_members
            )

        # Combine lists
        aggregated.active_members = [
            m for d in branch_metrics for m in d.active_members
        ]
        aggregated.active_contracts = [
            c for d in branch_metrics for c in d.active_contracts
        ]
        aggregated.prospects = [p for d in branch_metrics for p in d.prospects]
        aggregated.non_renewed_members = [
            m for d in branch_metrics for m in d.non_renewed_members
        ]
        aggregated.receivables = [r for d in branch_metrics for r in d.receivables]
        aggregated.recent_entries = [
            e for d in branch_metrics for e in d.recent_entries
        ]
        aggregated.cross_branch_entries = [
            e for d in branch_metrics for e in d.cross_branch_entries
        ]

        return aggregated
