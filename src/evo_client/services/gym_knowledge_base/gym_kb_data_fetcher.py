from typing import List, Dict, Optional
from evo_client.models.gym_model import GymKnowledgeBase, GymUnitKnowledgeBase, Address, BusinessHours
from evo_client.services.data_fetchers.configuration_data_fetcher import ConfigurationDataFetcher
from evo_client.services.data_fetchers.activity_data_fetcher import ActivityDataFetcher
from evo_client.services.data_fetchers.service_data_fetcher import ServiceDataFetcher
from evo_client.services.data_fetchers.membership_data_fetcher import MembershipDataFetcher
from evo_client.core.api_client import ApiClient
from evo_client.services.data_fetchers import BaseDataFetcher


class GymKnowledgeBaseService(BaseDataFetcher):
    """Service for building and maintaining the gym knowledge base."""
    
    @classmethod
    def create(
        cls,
        configuration_api,
        activity_api,
        service_api,
        membership_api,
        branch_api_clients: Optional[Dict[str, ApiClient]] = None
    ) -> "GymKnowledgeBaseService":
        """Create an instance of GymKnowledgeBaseService with initialized data fetchers."""
        return cls(
            configuration_fetcher=ConfigurationDataFetcher(configuration_api, branch_api_clients),
            activity_fetcher=ActivityDataFetcher(activity_api, branch_api_clients),
            service_fetcher=ServiceDataFetcher(service_api, branch_api_clients),    
            membership_fetcher=MembershipDataFetcher(membership_api, branch_api_clients)
        )

    def __init__(
        self,
        configuration_fetcher: ConfigurationDataFetcher,
        activity_fetcher: ActivityDataFetcher,
        service_fetcher: ServiceDataFetcher,
        membership_fetcher: MembershipDataFetcher,
    ):
        self.configuration_fetcher = configuration_fetcher
        self.activity_fetcher = activity_fetcher
        self.service_fetcher = service_fetcher
        self.membership_fetcher = membership_fetcher

    def build_knowledge_base(self) -> GymKnowledgeBase:
        """Build a complete knowledge base for the gym chain."""
        # Fetch all branch configurations
        branch_configs = self.configuration_fetcher.fetch_branch_configurations()
        if not branch_configs:
            raise ValueError("No branch configurations found")

        # Fetch all data once
        activities_data = self.activity_fetcher.fetch_activities_with_schedule()
        services = self.service_fetcher.fetch_services(active=True)
        plans = self.membership_fetcher.fetch_memberships(active=True)
        assert isinstance(plans, List)

        # Build knowledge base for each unit
        units = []
        for config in branch_configs:
            branch_id = config.id_branch
            unit_kb = GymUnitKnowledgeBase(
                unit_id=branch_id or 0,
                name=config.name or "",
                address=Address(
                    street=config.address or "",
                    number=config.number or "",
                    neighborhood=config.neighborhood or "",
                    city=config.city or "",
                    state=config.state_short or "",
                    postal_code=config.zip_code or "",
                    phone=config.telephone
                ),
                businessHours=[
                    BusinessHours(
                        weekDay=hours.week_day or "",
                        hoursFrom=str(hours.hours_from) if hours.hours_from else "",
                        hoursTo=str(hours.hours_to) if hours.hours_to else ""
                    )
                    for hours in config.business_hours or []
                ],
                activities=[a for a in activities_data['activities'] if a.id_branch == branch_id],
                availableServices=[s for s in services if s.id_branch == branch_id],
                plans=[p for p in plans if p.id_branch == branch_id],
                branchConfig=config,
                paymentPolicy={}
            )
            units.append(unit_kb)

        return GymKnowledgeBase(
            name=branch_configs[0].name.split()[0] if branch_configs[0].name else "",
            units=units,
            faqs=[]
        )
