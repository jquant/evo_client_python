"""Clean synchronous Activities API."""

from datetime import datetime
from typing import Any, List, Optional, cast

from ...models.atividade_agenda_api_view_model import AtividadeAgendaApiViewModel
from ...models.atividade_basico_api_view_model import AtividadeBasicoApiViewModel
from ...models.atividade_list_api_view_model import AtividadeListApiViewModel
from ...models.atividade_lugar_reserva_api_view_model import (
    AtividadeLugarReservaApiViewModel,
)
from ...models.common_models import ActivityOperationResponse
from ...models.e_origem_agendamento import EOrigemAgendamento
from ...models.e_status_atividade_sessao import EStatusAtividadeSessao
from .base import SyncBaseApi


class SyncActivitiesApi(SyncBaseApi):
    """Clean synchronous Activities API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/activities"

    def get_activities(
        self,
        search: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
    ) -> List[AtividadeListApiViewModel]:
        """
        Get activities list with optional filtering.

        Args:
            search: Filter by activity name, group name or tags
            branch_id: Filter by membership branch ID
            take: Number of records to return
            skip: Number of records to skip

        Returns:
            List of activities matching the criteria

        Example:
            >>> with SyncActivitiesApi() as api:
            ...     activities = api.get_activities(
            ...         search="yoga",
            ...         branch_id=1,
            ...         take=10
            ...     )
            ...     for activity in activities:
            ...         print(f"{activity.name} - {activity.description}")
        """
        params = {"search": search, "idBranch": branch_id, "take": take, "skip": skip}

        result = self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[AtividadeListApiViewModel],
            auth_settings=["Basic"],
        )
        return cast(List[AtividadeListApiViewModel], result)

    def get_schedule(
        self,
        member_id: Optional[int] = None,
        date: Optional[datetime] = None,
        branch_id: Optional[int] = None,
        activity_ids: Optional[List[int]] = None,
        audience_ids: Optional[List[int]] = None,
        take: Optional[int] = None,
        only_availables: bool = False,
        show_full_week: bool = False,
        branch_token: Optional[str] = None,
    ) -> List[AtividadeAgendaApiViewModel]:
        """
        Get activity schedule.

        Args:
            member_id: Filter by member ID
            date: Filter by specific date
            branch_id: Filter by branch ID
            activity_ids: Filter by activity IDs
            audience_ids: Filter by audience IDs
            take: Number of records to return
            only_availables: Show only available slots
            show_full_week: Show full week schedule
            branch_token: Branch access token

        Returns:
            List of scheduled activities

        Example:
            >>> from datetime import datetime
            >>> with SyncActivitiesApi() as api:
            ...     schedule = api.get_schedule(
            ...         member_id=123,
            ...         date=datetime(2024, 12, 20),
            ...         only_availables=True,
            ...         take=20
            ...     )
            ...     for activity in schedule:
            ...         print(f"{activity.name} at {activity.start_time}")
        """
        params = {
            "idMember": member_id,
            "date": date.isoformat() if date else None,
            "idBranch": branch_id,
            "idActivities": ",".join(map(str, activity_ids)) if activity_ids else None,
            "idAudiences": ",".join(map(str, audience_ids)) if audience_ids else None,
            "take": take,
            "onlyAvailables": only_availables,
            "showFullWeek": show_full_week,
            "branchToken": branch_token,
        }

        result = self.api_client.call_api(
            resource_path=f"{self.base_path}/schedule",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[AtividadeAgendaApiViewModel],
            auth_settings=["Basic"],
        )
        return cast(List[AtividadeAgendaApiViewModel], result)

    def get_schedule_detail(
        self,
        config_id: Optional[int] = None,
        activity_date: Optional[datetime] = None,
        session_id: Optional[int] = None,
    ) -> AtividadeBasicoApiViewModel:
        """
        Get activity schedule details.

        Args:
            config_id: Activity configuration ID (required with activity_date)
            activity_date: Activity date (required with config_id)
            session_id: Activity session ID (alternative to config_id/activity_date)

        Returns:
            Activity schedule details

        Raises:
            ValueError: If neither (config_id + activity_date) nor session_id provided

        Example:
            >>> from datetime import datetime
            >>> with SyncActivitiesApi() as api:
            ...     # Option 1: Using config_id and date
            ...     detail = api.get_schedule_detail(
            ...         config_id=123,
            ...         activity_date=datetime(2024, 12, 20)
            ...     )
            ...     # Option 2: Using session_id
            ...     detail = api.get_schedule_detail(session_id=456)
        """
        if not ((config_id and activity_date) or session_id):
            raise ValueError(
                "Either provide both config_id and activity_date, or session_id"
            )

        params = {
            "idConfiguration": config_id,
            "activityDate": activity_date.isoformat() if activity_date else None,
            "idActivitySession": session_id,
        }

        result = self.api_client.call_api(
            resource_path=f"{self.base_path}/schedule/detail",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=AtividadeBasicoApiViewModel,
            auth_settings=["Basic"],
        )
        return cast(AtividadeBasicoApiViewModel, result)

    def enroll(
        self,
        config_id: int,
        activity_date: datetime,
        member_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        slot_number: Optional[int] = None,
        origin: Optional[EOrigemAgendamento] = None,
    ) -> Any:
        """
        Enroll member in activity schedule.

        Args:
            config_id: Activity configuration ID
            activity_date: Activity schedule date
            member_id: Member ID (required if prospect_id is null)
            prospect_id: Prospect ID (required if member_id is null)
            slot_number: Slot number for reservation
            origin: Origin of enrollment

        Returns:
            Enrollment result

        Example:
            >>> from datetime import datetime
            >>> with SyncActivitiesApi() as api:
            ...     date = datetime(2024, 12, 20, 10, 30)
            ...     result = api.enroll(
            ...         config_id=123,
            ...         activity_date=date,
            ...         member_id=456
            ...     )
        """
        params = {
            "idConfiguration": config_id,
            "activityDate": activity_date.isoformat(),
            "idMember": member_id,
            "idProspect": prospect_id,
            "slotNumber": slot_number,
            "origin": origin.value if origin else None,
        }

        result = self.api_client.call_api(
            resource_path=f"{self.base_path}/schedule/enroll",
            method="POST",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=None,
            auth_settings=["Basic"],
        )
        return result

    def get_unavailable_spots(
        self, config_id: int, date: datetime
    ) -> List[AtividadeLugarReservaApiViewModel]:
        """
        Get list of unavailable spots for an activity session.

        Args:
            config_id: Activity configuration ID
            date: Activity schedule date

        Returns:
            List of unavailable spot reservations

        Example:
            >>> from datetime import datetime
            >>> with SyncActivitiesApi() as api:
            ...     date = datetime(2024, 1, 15)
            ...     spots = api.get_unavailable_spots(123, date)
            ...     for spot in spots:
            ...         print(f"Reserved spot: {spot.spot_number}")
        """
        params = {
            "idConfiguration": config_id,
            "date": date.isoformat(),
        }

        result = self.api_client.call_api(
            resource_path=f"{self.base_path}/list-unavailable-spots",
            method="GET",
            query_params=params,
            response_type=List[AtividadeLugarReservaApiViewModel],
            auth_settings=["Basic"],
        )
        return cast(List[AtividadeLugarReservaApiViewModel], result)

    def change_status(
        self,
        status: EStatusAtividadeSessao,
        member_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        config_id: Optional[int] = None,
        activity_date: Optional[datetime] = None,
        session_id: Optional[int] = None,
    ) -> ActivityOperationResponse:
        """
        Change status of a member in activity schedule.

        Args:
            status: New status (Attending=0, Absent=1, Justified absence=2)
            member_id: Member ID
            prospect_id: Prospect ID
            config_id: Activity configuration ID (only used when session_id is null)
            activity_date: Activity schedule date (only used when session_id is null)
            session_id: Activity session ID

        Returns:
            Operation result with success status

        Example:
            >>> from datetime import datetime
            >>> with SyncActivitiesApi() as api:
            ...     date = datetime(2024, 1, 15)
            ...     result = api.change_status(
            ...         status=EStatusAtividadeSessao.ATTENDING,
            ...         member_id=123,
            ...         config_id=456,
            ...         activity_date=date
            ...     )
            ...     if result.success:
            ...         print("Status changed successfully")
        """
        params = {
            "status": status.value,
            "idMember": member_id,
            "idProspect": prospect_id,
            "idConfiguration": config_id,
            "activityDate": activity_date.isoformat() if activity_date else None,
            "idActivitySession": session_id,
        }

        try:
            self.api_client.call_api(
                resource_path=f"{self.base_path}/schedule/enroll/change-status",
                method="POST",
                query_params={k: v for k, v in params.items() if v is not None},
                response_type=None,
                auth_settings=["Basic"],
            )

            return ActivityOperationResponse(
                success=True,
                activitySessionId=session_id,
                memberId=member_id,
                prospectId=prospect_id,
                status=status.name,
                message="Activity status changed successfully",
            )
        except Exception as e:
            return ActivityOperationResponse(
                success=False,
                activitySessionId=session_id,
                memberId=member_id,
                prospectId=prospect_id,
                message=f"Error changing activity status: {str(e)}",
                errors=[str(e)],
            )

    def create_experimental_class(
        self,
        prospect_id: int,
        activity_date: datetime,
        activity: str,
        service: str,
        activity_exists: bool = False,
        branch_id: Optional[int] = None,
    ) -> bool:
        """
        Create a new experimental class and enroll prospect.

        Args:
            prospect_id: ID of prospect who will participate
            activity_date: Activity schedule date and time
            activity: Activity name
            service: Service that will be sold to allow the trial class
            activity_exists: Whether activity exists
            branch_id: Branch ID

        Returns:
            True if experimental class was created successfully

        Example:
            >>> from datetime import datetime
            >>> with SyncActivitiesApi() as api:
            ...     date = datetime(2024, 1, 15, 10, 30)
            ...     success = api.create_experimental_class(
            ...         prospect_id=123,
            ...         activity_date=date,
            ...         activity="Yoga",
            ...         service="Trial Class"
            ...     )
            ...     if success:
            ...         print("Experimental class created")
        """
        params = {
            "idProspect": prospect_id,
            "activityDate": activity_date.isoformat(),
            "activity": activity,
            "service": service,
            "activityExists": activity_exists,
            "idBranch": branch_id,
        }

        result: Any = self.api_client.call_api(
            resource_path=f"{self.base_path}/schedule/experimental-class",
            method="POST",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=None,  # Returns boolean
            auth_settings=["Basic"],
        )
        return cast(bool, result)
