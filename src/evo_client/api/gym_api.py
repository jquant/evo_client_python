# /src/evo_client/api/gym_api.py

from __future__ import absolute_import

from datetime import datetime, timedelta
from decimal import Decimal
from multiprocessing.pool import Pool
from typing import Any, Dict, List, Optional, TypeVar

from loguru import logger

from ..core.api_client import ApiClient
from ..core.configuration import Configuration
from ..models.receivables_api_view_model import ReceivablesApiViewModel
from ..services.data_fetchers.activity_data_fetcher import ActivityDataFetcher
from ..services.data_fetchers.configuration_data_fetcher import ConfigurationDataFetcher
from ..services.data_fetchers.entries_data_fetcher import EntriesDataFetcher

# Import data fetchers
from ..services.data_fetchers.member_data_fetcher import MemberDataFetcher
from ..services.data_fetchers.membership_data_fetcher import MembershipDataFetcher
from ..services.data_fetchers.prospects_data_fetcher import ProspectsDataFetcher
from ..services.data_fetchers.receivables_data_fetcher import ReceivablesDataFetcher
from ..services.data_fetchers.service_data_fetcher import ServiceDataFetcher
from ..services.data_fetchers.sales_data_fetcher import SalesDataFetcher
from ..services.gym_knowledge_base.gym_kb_data_fetcher import GymKnowledgeBaseService

# Models from gym_model
try:
    from ..models.gym_model import (
        # Core models
        GymKnowledgeBase,
        OverdueMember,
    )
except ImportError as e:
    logger.error(f"Error importing gym_model: {str(e)}")
    raise

# API clients
from ..api.activities_api import ActivitiesApi
from ..api.configuration_api import ConfigurationApi
from ..api.employees_api import EmployeesApi
from ..api.entries_api import EntriesApi
from ..api.managment_api import ManagementApi
from ..api.member_membership_api import MemberMembershipApi
from ..api.members_api import MembersApi
from ..api.membership_api import MembershipApi
from ..api.prospects_api import ProspectsApi
from ..api.receivables_api import ReceivablesApi
from ..api.sales_api import SalesApi
from ..api.service_api import ServiceApi
from ..api.webhook_api import WebhookApi
from ..api.workout_api import WorkoutApi

T = TypeVar('T')

class GymApi:
    """Gym API client for EVO API."""
    _pool: Pool
    branch_ids: List[int]

    def __init__(
        self,
        api_client: Optional[ApiClient] = None,
        branch_api_clients: Optional[Dict[str, ApiClient]] = None,
        branch_credentials: Optional[List[Dict[str, str]]] = None
    ):
        """Initialize the gym API.
        
        Args:
            api_client: The default API client
            branch_api_clients: Optional dictionary mapping branch IDs to their API clients
            branch_credentials: Optional list of branch credentials (deprecated, use branch_api_clients)
        """
        if branch_credentials:
            # Convert branch_credentials to branch_api_clients
            branch_api_clients = {}
            for cred in branch_credentials:
                config = Configuration()
                config.username = cred['username']
                config.password = cred['password']
                branch_api_clients[cred['branch_id']] = ApiClient(configuration=config)
            
            # Use first branch client as default if none provided
            if api_client is None and branch_api_clients:
                api_client = next(iter(branch_api_clients.values()))

        if api_client is None:
            config = Configuration()
            api_client = ApiClient(configuration=config)

        self.api_client = api_client
        self.branch_api_clients = branch_api_clients or {}
        self._pool = Pool(processes=1)  # Single process pool for async operations
        
        # Store branch IDs as integers
        self.branch_ids = [int(bid) for bid in self.branch_api_clients.keys()] if branch_api_clients else []
        
        # Initialize API instances with branch awareness
        self.configuration_api = ConfigurationApi(api_client=api_client)
        self.activities_api = ActivitiesApi(api_client=api_client)
        self.membership_api = MembershipApi(api_client=api_client)
        self.entries_api = EntriesApi(api_client=api_client)
        self.member_membership_api = MemberMembershipApi(api_client=api_client)
        self.workout_api = WorkoutApi(api_client=api_client)
        self.service_api = ServiceApi(api_client=api_client)
        self.employees_api = EmployeesApi(api_client=api_client)
        self.receivables_api = ReceivablesApi(api_client=api_client)
        self.sales_api = SalesApi(api_client=api_client)
        self.management_api = ManagementApi(api_client=api_client)
        self.members_api = MembersApi(api_client=api_client)
        self.prospects_api = ProspectsApi(api_client=api_client)
        self.webhook_api = WebhookApi(api_client=api_client)
        
        # Initialize data fetchers with branch awareness
        self.configuration_data_fetcher = ConfigurationDataFetcher(
            configuration_api=self.configuration_api,
            branch_api_clients=self.branch_api_clients
        )
        self.member_data_fetcher = MemberDataFetcher(
            members_api=self.members_api,
            branch_api_clients=self.branch_api_clients
        )
        self.receivables_data_fetcher = ReceivablesDataFetcher(
            receivables_api=self.receivables_api,
            branch_api_clients=self.branch_api_clients
        )
        self.entries_data_fetcher = EntriesDataFetcher(
            self.entries_api, 
            self.branch_api_clients
        )
        self.prospects_data_fetcher = ProspectsDataFetcher(
            self.prospects_api, 
            self.branch_api_clients
        )
        self.activity_data_fetcher = ActivityDataFetcher(
            self.activities_api, 
            self.branch_api_clients
        )
        self.service_data_fetcher = ServiceDataFetcher(
            self.service_api, 
            self.branch_api_clients
        )
        self.membership_data_fetcher = MembershipDataFetcher(
            self.membership_api, 
            self.branch_api_clients
        )
        self.sales_data_fetcher = SalesDataFetcher(
            self.sales_api, 
            self.branch_api_clients
        )
        self.knowledge_base_fetcher = GymKnowledgeBaseService(
            configuration_fetcher=self.configuration_data_fetcher,
            activity_fetcher=self.activity_data_fetcher,
            service_fetcher=self.service_data_fetcher,
            membership_fetcher=self.membership_data_fetcher,
            branch_api_clients=self.branch_api_clients
        )

    def __del__(self):
        """Clean up resources."""
        if hasattr(self, '_pool'):
            self._pool.close()
            self._pool.join()

    def get_overdue_members(
        self,
        min_days_overdue: int = 1,
        branch_ids: Optional[List[int]] = None
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

    def _group_overdue_receivables(self, receivables: List[ReceivablesApiViewModel]) -> List[OverdueMember]:
        """Group overdue receivables by member and branch."""
        member_map: Dict[tuple[int, Optional[int]], OverdueMember] = {}
        
        # Keep track of processed receivable IDs to avoid duplicates
        processed_receivables = set()
        
        for receivable in receivables:
            # Skip if we've already processed this receivable
            if receivable.id_receivable in processed_receivables:
                continue
                
            if not receivable.id_member_payer:
                logger.warning(f"Receivable {receivable.id_receivable} has no member payer")
                continue
                
            key = (receivable.id_member_payer, receivable.id_branch_member)
            processed_receivables.add(receivable.id_receivable)
            
            if key not in member_map:
                member_map[key] = OverdueMember(
                    id=receivable.id_receivable or 0,
                    name=receivable.payer_name or "Unknown", 
                    member_id=receivable.id_member_payer,
                    total_overdue=Decimal('0.00'),
                    overdue_since=receivable.due_date or datetime.now(),
                    overdue_receivables=[],
                    branch_id=receivable.id_branch_member,
                    last_payment_date=None
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
