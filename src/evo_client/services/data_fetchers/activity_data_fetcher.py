from typing import List, Optional, Dict
from datetime import datetime

from ...api.activities_api import ActivitiesApi
from ...models.atividade_list_api_view_model import AtividadeListApiViewModel
from ...models.atividade_sessao_participante_api_view_model import (
    AtividadeSessaoParticipanteApiViewModel,
)
from ...utils.pagination_utils import paginated_api_call
from ...core.api_client import ApiClient
from . import BaseDataFetcher
from loguru import logger


class ActivityDataFetcher(BaseDataFetcher[ActivitiesApi]):
    """Handles fetching and processing activity-related data."""

    def __init__(
        self,
        activities_api: ActivitiesApi,
        branch_api_clients: Optional[Dict[str, ApiClient]] = None,
    ):
        """Initialize the activity data fetcher.

        Args:
            activities_api: The activities API instance
            branch_api_clients: Optional dictionary mapping branch IDs to their API clients
        """
        super().__init__(activities_api, branch_api_clients)

    def fetch_activities_with_schedule(
        self,
        # Activity filters
        search: Optional[str] = None,
        # Schedule filters
        activity_date: Optional[datetime] = None,
        id_member: Optional[int] = None,
        default_client: bool = True,
    ) -> Dict[str, List]:
        """Fetch activities and their schedules with various filters.

        Args:
            search: Filter activities by name, group name or tags
            activity_date: Filter schedule by activity date
            id_member: Filter schedule by member ID
            status: Filter schedule by status codes:
                0: Free
                1: Available
                2: Full
                3: Booking Closed
                4: Restricted
                5: Registered
                6: Finished
                7: Canceled
                8: In Queue
                10: Free Closed
                11: Restricted Closed
                12: Restricted No Participation
                15: Full No Waiting List

        Returns:
            Dict containing:
                'activities': List[AtividadeListApiViewModel] - List of activities
                'schedules': List[AtividadeSessaoParticipanteApiViewModel] - List of scheduled activities
        """
        # Use available branch IDs from base class
        branch_ids = self.get_available_branch_ids()

        if default_client:
            activities = paginated_api_call(
                api_func=self.api.get_activities,
                unit_id="default",
                search=search,
                supports_pagination=False,
            )
        else:
            activities = []
            for branch_id in branch_ids:
                branch_api = self.get_branch_api(branch_id, ActivitiesApi)
                if branch_api:
                    result = paginated_api_call(
                        api_func=branch_api.get_activities,
                        unit_id=str(branch_id),
                        search=search,
                        supports_pagination=False,
                    )
                    activities.extend(result)

        # For each branch, get its specific schedule
        if default_client:
            schedules = paginated_api_call(
                api_func=self.api.get_schedule,
                unit_id="default",
                show_full_week=True,
                date=activity_date,
                member_id=id_member,
                supports_pagination=False,
            )

        else:
            schedules = []
            for branch_id in branch_ids:
                branch_api = self.get_branch_api(branch_id, ActivitiesApi)
                if branch_api:
                    try:
                        branch_schedules = paginated_api_call(
                            api_func=branch_api.get_schedule,
                            unit_id=str(branch_id),
                            show_full_week=True,
                            date=activity_date,
                            member_id=id_member,
                            supports_pagination=False,
                        )
                        if branch_schedules:
                            schedules.extend(branch_schedules)
                    except Exception as e:
                        logger.warning(
                            f"Failed to fetch schedules for branch {branch_id}: {e}"
                        )

        # Convert raw data to dictionaries first, then to models
        return {
            "activities": [
                AtividadeListApiViewModel(**activity.to_dict())
                for activity in activities
            ],
            "schedules": [
                AtividadeSessaoParticipanteApiViewModel(**schedule.to_dict())
                for schedule in schedules
            ],
        }
