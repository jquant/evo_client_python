import json
from pathlib import Path
from typing import List

from loguru import logger

from ...models.configuracao_api_view_model import ConfiguracaoApiViewModel
from ...models.gym_model import (
    Address,
    BusinessHours,
    GymKnowledgeBase,
    GymUnitKnowledgeBase,
)
from ..data_fetchers import BranchApiClientManager
from ..data_fetchers.activity_data_fetcher import ActivityDataFetcher
from ..data_fetchers.configuration_data_fetcher import ConfigurationDataFetcher
from ..data_fetchers.membership_data_fetcher import MembershipDataFetcher
from ..data_fetchers.service_data_fetcher import ServiceDataFetcher


class GymKnowledgeBaseService:
    """Service for building and maintaining the gym knowledge base."""

    def __init__(self, client_manager: BranchApiClientManager):
        """Initialize the knowledge base service.

        Args:
            client_manager: The client manager instance
        """
        self.client_manager = client_manager
        self.configuration_fetcher = ConfigurationDataFetcher(client_manager)
        self.activity_fetcher = ActivityDataFetcher(client_manager)
        self.service_fetcher = ServiceDataFetcher(client_manager)
        self.membership_fetcher = MembershipDataFetcher(client_manager)

    def build_knowledge_base(self) -> GymKnowledgeBase:
        """Build a complete knowledge base for the gym chain."""
        try:
            # Get cached configurations from file instead of fetching
            config_dir = Path(".config")
            cred_files = list(config_dir.glob("credentials.*.json"))

            if not cred_files:
                raise ValueError("No credential files found")

            # Read cached configurations
            gym_name = cred_files[0].stem.split(".")[1]
            config_file = config_dir / f"branch_configs.{gym_name}.json"

            if not config_file.exists():
                logger.warning("No cached configurations found, fetching from API...")
                branch_configs = (
                    self.configuration_fetcher.validate_and_cache_configurations()
                )
            else:
                with open(config_file) as f:
                    cache_data = json.load(f)
                    branch_configs = [
                        ConfiguracaoApiViewModel(**config)
                        for config in cache_data["configurations"]
                    ]

            if not branch_configs:
                raise ValueError("No branch configurations found")

            # Fetch all data with retry logic
            logger.info("Fetching activities data...")
            activities_data = self.activity_fetcher.fetch_activities_with_schedule()
            logger.info(
                f"Fetched {len(activities_data['activities'])} activities across all branches"
            )
            logger.info(
                f"Fetched {len(activities_data['schedules'])} schedules across all branches"
            )

            logger.info("Fetching services data...")
            services = self.service_fetcher.fetch_services(active=True) or []
            logger.info(f"Fetched {len(services)} services across all branches")

            logger.info("Fetching membership plans...")
            plans = self.membership_fetcher.fetch_memberships(active=True) or []
            if isinstance(plans, List):
                logger.info(f"Fetched {len(plans)} plans across all branches")

            # Build knowledge base for each unit
            units = []
            branch_ids = self.configuration_fetcher.get_available_branch_ids()

            for config in branch_configs:
                branch_id = config.id_branch
                if not branch_id or branch_id not in branch_ids:
                    continue

                unit_kb = GymUnitKnowledgeBase(
                    branch_id=branch_id,
                    name=config.name or "",
                    address=Address(
                        street=config.address or "",
                        number=config.number or "",
                        neighborhood=config.neighborhood or "",
                        city=config.city or "",
                        state=config.state_short or "",
                        postal_code=config.zip_code or "",
                        phone=config.telephone,
                    ),
                    businessHours=[
                        BusinessHours(
                            weekDay=hours.week_day or "",
                            hoursFrom=(
                                str(hours.hours_from) if hours.hours_from else ""
                            ),
                            hoursTo=str(hours.hours_to) if hours.hours_to else "",
                        )
                        for hours in config.business_hours or []
                    ],
                    activities=[
                        a
                        for a in activities_data["activities"]
                        if a.id_branch == branch_id
                    ],
                    availableServices=[s for s in services if s.id_branch == branch_id],
                    plans=[p for p in plans if p.id_branch == branch_id],
                    branchConfig=config,
                    paymentPolicy={},
                )
                units.append(unit_kb)

            if not units:
                raise ValueError("No units found for the available branch IDs")

            return GymKnowledgeBase(
                name=(
                    branch_configs[0].name.split()[0] if branch_configs[0].name else ""
                ),
                units=units,
                faqs=[],
            )

        except Exception as e:
            logger.error(f"Error building knowledge base: {str(e)}")
            raise ValueError(f"Error building knowledge base: {str(e)}")
