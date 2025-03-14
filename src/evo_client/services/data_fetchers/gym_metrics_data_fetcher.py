from datetime import datetime, timedelta
from typing import List, Optional

from ...models.gym_model import GymOperatingData
from ...services.operating_data.operating_data_computer import OperatingDataComputer
from . import BaseDataFetcher
from .activity_data_fetcher import ActivityDataFetcher
from .configuration_data_fetcher import ConfigurationDataFetcher
from .entries_data_fetcher import EntriesDataFetcher
from .member_data_fetcher import MemberDataFetcher
from .membership_data_fetcher import MembershipDataFetcher
from .prospects_data_fetcher import ProspectsDataFetcher
from .receivables_data_fetcher import ReceivablesDataFetcher
from .sales_data_fetcher import SalesDataFetcher


class GymMetricsDataFetcher(BaseDataFetcher):
    """
    Provides advanced KPI computations like churn, MRR, LTV, GRR, NRR.
    Fetch current and previous month data and compute metrics using OperatingDataComputer.
    """

    def __init__(self, client_manager):
        super().__init__(client_manager)
        self.member_fetcher = MemberDataFetcher(client_manager)
        self.membership_fetcher = MembershipDataFetcher(client_manager)
        self.prospects_fetcher = ProspectsDataFetcher(client_manager)
        self.receivables_fetcher = ReceivablesDataFetcher(client_manager)
        self.entries_fetcher = EntriesDataFetcher(client_manager)
        self.sales_fetcher = SalesDataFetcher(client_manager)
        self.configuration_fetcher = ConfigurationDataFetcher(client_manager)
        self.activity_fetcher = ActivityDataFetcher(client_manager)
        self.computer = OperatingDataComputer()

    def fetch_advanced_metrics(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        branch_ids: Optional[List[int]] = None,
    ) -> GymOperatingData:
        """
        Fetch advanced metrics by comparing current and previous month's data.
        If no previous month data is available, we default GRR and NRR to 100%.

        Steps:
        - Determine date range if not provided: last 30 days by default.
        - Fetch current data: active_members, prospects, non_renewed, receivables, entries, active_contracts.
        - Fetch previous month data similarly.
        - Use OperatingDataComputer to compute advanced metrics.

        Returns:
            GymOperatingData with advanced metrics filled in.
        """
        if branch_ids is None:
            branch_ids = self.get_available_branch_ids()

        if not from_date or not to_date:
            to_date = datetime.now()
            from_date = to_date - timedelta(days=30)

        # Previous month:
        prev_to_date = from_date
        prev_from_date = prev_to_date - timedelta(days=30)

        # Fetch current data
        active_members = self.member_fetcher.fetch_members(
            membership_start_date_start=from_date,
            membership_start_date_end=to_date,
            status=1,
        )
        non_renewed = self.member_fetcher.fetch_members(
            membership_cancel_date_start=from_date,
            membership_cancel_date_end=to_date,
            status=2,
        )
        prospects = self.prospects_fetcher.fetch_prospects(
            register_date_start=from_date, register_date_end=to_date
        )
        receivables = self.receivables_fetcher.fetch_receivables(
            due_date_start=from_date, due_date_end=to_date
        )
        entries = self.entries_fetcher.fetch_entries(
            register_date_start=from_date, register_date_end=to_date
        )
        # fetch memberships (active contracts)
        active_contracts = self.membership_fetcher.fetch_memberships(active=True)

        # Fetch previous data
        prev_active_members = self.member_fetcher.fetch_members(
            membership_start_date_start=prev_from_date,
            membership_start_date_end=prev_to_date,
            status=1,
        )
        prev_non_renewed = self.member_fetcher.fetch_members(
            membership_cancel_date_start=prev_from_date,
            membership_cancel_date_end=prev_to_date,
            status=2,
        )
        prev_prospects = self.prospects_fetcher.fetch_prospects(
            register_date_start=prev_from_date, register_date_end=prev_to_date
        )
        prev_receivables = self.receivables_fetcher.fetch_receivables(
            due_date_start=prev_from_date, due_date_end=prev_to_date
        )
        prev_entries = self.entries_fetcher.fetch_entries(
            register_date_start=prev_from_date, register_date_end=prev_to_date
        )
        prev_active_contracts = self.membership_fetcher.fetch_memberships(active=True)

        previous_data = self.computer.compute_metrics(
            active_members=prev_active_members,
            prospects=prev_prospects,
            non_renewed=prev_non_renewed,
            receivables=prev_receivables,
            entries=prev_entries,
            active_contracts=prev_active_contracts,
            from_date=prev_from_date,
            to_date=prev_to_date,
            previous_data=None,  # no data before previous
        )

        current_data = self.computer.compute_metrics(
            active_members=active_members,
            prospects=prospects,
            non_renewed=non_renewed,
            receivables=receivables,
            entries=entries,
            active_contracts=active_contracts,
            from_date=from_date,
            to_date=to_date,
            previous_data=previous_data,
        )

        return current_data
