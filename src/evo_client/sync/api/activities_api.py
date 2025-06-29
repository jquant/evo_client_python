"""Clean synchronous Activities API."""

from datetime import datetime
from typing import Any, List, Optional, cast

from ...models.atividade_agenda_api_view_model import AtividadeAgendaApiViewModel
from ...models.atividade_basico_api_view_model import AtividadeBasicoApiViewModel
from ...models.atividade_list_api_view_model import AtividadeListApiViewModel
from ...models.atividade_sessao_participante_api_view_model import (
    AtividadeSessaoParticipanteApiViewModel,
)
from ...models.atividade_lugar_reserva_api_view_model import (
    AtividadeLugarReservaApiViewModel,
)
from ...models.e_origem_agendamento import EOrigemAgendamento
from ...models.e_status_atividade_sessao import EStatusAtividadeSessao
from ...models.common_models import ActivityOperationResponse
from .base import SyncBaseApi


class SyncActivitiesApi(SyncBaseApi):
    """Clean synchronous Activities API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/activities"

    def get_activities(
        self,
        activity_name: Optional[str] = None,
        is_visible: Optional[bool] = None,
        branch_id: Optional[int] = None,
    ) -> List[AtividadeListApiViewModel]:
        """
        Get activities list with optional filtering.

        Args:
            activity_name: Filter by activity name
            is_visible: Filter by visibility
            branch_id: Filter by branch ID

        Returns:
            List of activities

        Example:
            >>> with SyncActivitiesApi() as api:
            ...     activities = api.get_activities(is_visible=True)
            ...     for activity in activities:
            ...         print(f"Activity: {activity.name}")
        """
        params = {
            "activityName": activity_name,
            "isVisible": is_visible,
            "idBranch": branch_id,
        }

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
        start_date: datetime,
        end_date: datetime,
        member_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        activity_name: Optional[str] = None,
        branch_id: Optional[int] = None,
    ) -> List[AtividadeAgendaApiViewModel]:
        """
        Get activity schedule.

        Args:
            start_date: Start date for schedule
            end_date: End date for schedule
            member_id: Filter by member ID
            employee_id: Filter by employee ID
            activity_name: Filter by activity name
            branch_id: Filter by branch ID

        Returns:
            List of scheduled activities

        Example:
            >>> from datetime import datetime
            >>> with SyncActivitiesApi() as api:
            ...     start = datetime(2024, 1, 1)
            ...     end = datetime(2024, 1, 31)
            ...     schedule = api.get_schedule(start, end, member_id=123)
            ...     for item in schedule:
            ...         print(f"Activity: {item.activity_name} at {item.start_time}")
        """
        params = {
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
            "idMember": member_id,
            "idEmployee": employee_id,
            "activityName": activity_name,
            "idBranch": branch_id,
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
        self, configuration_id: int, date: datetime
    ) -> List[AtividadeSessaoParticipanteApiViewModel]:
        """
        Get activity schedule details.

        Args:
            configuration_id: Activity configuration ID
            date: Activity date

        Returns:
            List of activity session participants

        Example:
            >>> from datetime import datetime
            >>> with SyncActivitiesApi() as api:
            ...     date = datetime(2024, 1, 15)
            ...     details = api.get_schedule_detail(123, date)
            ...     for participant in details:
            ...         print(f"Participant: {participant.member_name}")
        """
        params = {
            "idConfiguration": configuration_id,
            "date": date.isoformat(),
        }

        result = self.api_client.call_api(
            resource_path=f"{self.base_path}/schedule/detail",
            method="GET",
            query_params=params,
            response_type=List[AtividadeSessaoParticipanteApiViewModel],
            auth_settings=["Basic"],
        )
        return cast(List[AtividadeSessaoParticipanteApiViewModel], result)

    def enroll_in_activity(
        self,
        member_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        configuration_id: Optional[int] = None,
        activity_date: Optional[datetime] = None,
        slot_number: Optional[int] = None,
        origin: Optional[int] = None,
        enrollment_origin: Optional[EOrigemAgendamento] = None,
        spot: Optional[str] = None,
    ) -> bool:
        """
        Enroll member/prospect in activity.

        Args:
            member_id: Member ID (required if prospect_id is null)
            prospect_id: Prospect ID (required if member_id is null)
            configuration_id: Activity configuration identifier
            activity_date: Scheduled activity date
            slot_number: Slot number for the activity (for individual slot reservations)
            origin: Origin of the inscription/reservation
            activity_session_id: [DEPRECATED] Activity session ID - use configuration_id instead
            enrollment_origin: [DEPRECATED] Origin of enrollment - use origin instead
            spot: [DEPRECATED] Spot reservation - use slot_number instead

        Returns:
            True if enrollment was successful

        Example:
            >>> from datetime import datetime
            >>> with SyncActivitiesApi() as api:
            ...     date = datetime(2024, 1, 15, 10, 30)
            ...     success = api.enroll_in_activity(
            ...         member_id=123,
            ...         configuration_id=456,
            ...         activity_date=date,
            ...         slot_number=1,
            ...         origin=2
            ...     )
            ...     if success:
            ...         print("Enrolled successfully")
        """
        # Handle backward compatibility
        if enrollment_origin is not None and origin is None:
            origin = (
                enrollment_origin.value
                if hasattr(enrollment_origin, "value")
                else enrollment_origin
            )

        if spot is not None and slot_number is None:
            # Try to convert spot to slot_number if it's numeric
            try:
                slot_number = int(spot)
            except (ValueError, TypeError):
                pass

        params = {
            "idConfiguration": configuration_id,
            "activityDate": activity_date.isoformat() if activity_date else None,
            "slotNumber": slot_number,
            "idMember": member_id,
            "idProspect": prospect_id,
            "origin": origin,
        }

        result: Any = self.api_client.call_api(
            resource_path=f"{self.base_path}/schedule/enroll",
            method="POST",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=None,  # Returns boolean
            auth_settings=["Basic"],
        )
        return cast(bool, result)

    def change_activity_status(
        self,
        status: EStatusAtividadeSessao,
        member_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        configuration_id: Optional[int] = None,
        activity_date: Optional[datetime] = None,
        activity_session_id: Optional[int] = None,
    ) -> ActivityOperationResponse:
        """
        Change status of a member in activity schedule.

        Args:
            status: New status (Attending=0, Absent=1, Justified absence=2)
            member_id: Member ID
            prospect_id: Prospect ID
            configuration_id: Activity configuration ID (only used when activity_session_id is null)
            activity_date: Activity schedule date (only used when activity_session_id is null)
            activity_session_id: Activity session ID

        Returns:
            Operation result with success status

        Example:
            >>> from datetime import datetime
            >>> with SyncActivitiesApi() as api:
            ...     date = datetime(2024, 1, 15)
            ...     result = api.change_activity_status(
            ...         status=EStatusAtividadeSessao.ATTENDING,
            ...         member_id=123,
            ...         configuration_id=456,
            ...         activity_date=date
            ...     )
            ...     if result.success:
            ...         print("Status changed successfully")
        """
        params = {
            "status": status.value,
            "idMember": member_id,
            "idProspect": prospect_id,
            "idConfiguration": configuration_id,
            "activityDate": activity_date.isoformat() if activity_date else None,
            "idActivitySession": activity_session_id,
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
                activitySessionId=activity_session_id,
                memberId=member_id,
                prospectId=prospect_id,
                status=status.name,
                message="Activity status changed successfully",
            )
        except Exception as e:
            return ActivityOperationResponse(
                success=False,
                activitySessionId=activity_session_id,
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
        activity_exist: bool = False,
        branch_id: Optional[int] = None,
    ) -> bool:
        """
        Create a new experimental class and enroll prospect.

        Args:
            prospect_id: ID of prospect who will participate
            activity_date: Activity schedule date and time
            activity: Activity name
            service: Service that will be sold to allow the trial class
            activity_exist: Whether activity exists
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
            "activityExist": activity_exist,
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

    def get_unavailable_spots(
        self, configuration_id: int, date: datetime
    ) -> List[AtividadeLugarReservaApiViewModel]:
        """
        List spots that are already filled in the activity session.

        Args:
            configuration_id: Activity configuration ID
            date: Activity schedule date

        Returns:
            List of unavailable spots

        Example:
            >>> from datetime import datetime
            >>> with SyncActivitiesApi() as api:
            ...     date = datetime(2024, 1, 15)
            ...     spots = api.get_unavailable_spots(123, date)
            ...     for spot in spots:
            ...         print(f"Unavailable spot: {spot.spot}")
        """
        params = {
            "idConfiguration": configuration_id,
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
