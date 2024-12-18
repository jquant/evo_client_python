from typing import List, Optional, Dict
from ...models.gym_model import (
    GymKnowledgeBase,
    GymUnitKnowledgeBase,
    Address,
    BusinessHours,
)
from ..data_fetchers.configuration_data_fetcher import (
    ConfigurationDataFetcher,
)
from ..data_fetchers.activity_data_fetcher import ActivityDataFetcher
from ..data_fetchers.service_data_fetcher import ServiceDataFetcher
from ..data_fetchers.membership_data_fetcher import (
    MembershipDataFetcher,
)
from ...core.api_client import ApiClient
from ..data_fetchers import BaseDataFetcher
from ...api.configuration_api import ConfiguracaoApiViewModel

from loguru import logger
from pathlib import Path
import json


class GymKnowledgeBaseService(BaseDataFetcher):
    """Service for building and maintaining the gym knowledge base."""

    def __init__(
        self,
        configuration_fetcher: ConfigurationDataFetcher,
        activity_fetcher: ActivityDataFetcher,
        service_fetcher: ServiceDataFetcher,
        membership_fetcher: MembershipDataFetcher,
        branch_api_clients: Optional[Dict[str, ApiClient]] = None,
    ):
        """Initialize the knowledge base service.

        Args:
            configuration_fetcher: The configuration data fetcher
            activity_fetcher: The activity data fetcher
            service_fetcher: The service data fetcher
            membership_fetcher: The membership data fetcher
            branch_api_clients: Optional dictionary mapping branch IDs to their API clients
        """
        super().__init__(None, branch_api_clients)  # No direct API needed
        self.configuration_fetcher = configuration_fetcher
        self.activity_fetcher = activity_fetcher
        self.service_fetcher = service_fetcher
        self.membership_fetcher = membership_fetcher

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
            activities_data = self.activity_fetcher.fetch_activities_with_schedule(
                default_client=False
            )
            logger.info(
                f"Fetched {len(activities_data['activities'])} activities across all branches"
            )
            logger.info(
                f"Fetched {len(activities_data['schedules'])} schedules across all branches"
            )

            logger.info("Fetching services data...")
            services = (
                self.service_fetcher.fetch_services(active=True, default_client=False)
                or []
            )
            logger.info(f"Fetched {len(services)} services across all branches")

            logger.info("Fetching membership plans...")
            plans = (
                self.membership_fetcher.fetch_memberships(
                    active=True, default_client=False
                )
                or []
            )
            if isinstance(plans, List):
                logger.info(f"Fetched {len(plans)} plans across all branches")

            # Build knowledge base for each unit
            units = []
            branch_ids = self.get_available_branch_ids()

            for config in branch_configs:
                branch_id = config.id_branch
                if not branch_id or branch_id not in branch_ids:
                    continue

                unit_kb = GymUnitKnowledgeBase(
                    unit_id=branch_id,
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
