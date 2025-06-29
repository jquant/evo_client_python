from datetime import datetime
from typing import Dict, List, Optional

from ...models.atividade_list_api_view_model import AtividadeListApiViewModel
from ...models.atividade_sessao_participante_api_view_model import (
    AtividadeSessaoParticipanteApiViewModel,
)
from ...sync.api.activities_api import SyncActivitiesApi
from ...utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher


class ActivityDataFetcher(BaseDataFetcher):
    """Handles fetching and processing activity-related data."""

    def fetch_activities_with_schedule(
        self,
        # Activity filters
        search: Optional[str] = None,
        # Schedule filters
        activity_date: Optional[datetime] = None,
        id_member: Optional[int] = None,
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

        activities = []
        schedules = []
        for branch_id in branch_ids:
            branch_api = SyncActivitiesApi(api_client=self.get_branch_api(branch_id))
            if branch_api:
                result = paginated_api_call(
                    api_func=branch_api.get_activities,
                    branch_id=str(branch_id),
                    search=search,
                    supports_pagination=False,
                )
                activities.extend(result)

                branch_schedules = paginated_api_call(
                    api_func=branch_api.get_schedule,
                    branch_id=str(branch_id),
                    show_full_week=True,
                    date=activity_date,
                    member_id=id_member,
                    supports_pagination=False,
                )
                if branch_schedules:
                    schedules.extend(branch_schedules)

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
