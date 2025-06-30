"""Clean asynchronous Activities API."""

from datetime import datetime
from typing import Any, List, Optional, cast

from ...models.atividade_agenda_api_view_model import AtividadeAgendaApiViewModel
from ...models.atividade_basico_api_view_model import AtividadeBasicoApiViewModel
from ...models.atividade_list_api_view_model import AtividadeListApiViewModel
from ...models.e_origem_agendamento import EOrigemAgendamento
from ...models.e_status_atividade_sessao import EStatusAtividadeSessao
from .base import AsyncBaseApi


class AsyncActivitiesApi(AsyncBaseApi):
    """Clean asynchronous Activities API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path = "/api/v1/activities"

    async def get_activities(
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
            >>> async with AsyncActivitiesApi() as api:
            ...     activities = await api.get_activities(
            ...         search="yoga",
            ...         branch_id=1,
            ...         take=10
            ...     )
            ...     for activity in activities:
            ...         print(f"{activity.name} - {activity.description}")
        """
        params = {"search": search, "idBranch": branch_id, "take": take, "skip": skip}

        result = await self.api_client.call_api(
            resource_path=self.base_path,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[AtividadeListApiViewModel],
            auth_settings=["Basic"],
        )
        return cast(List[AtividadeListApiViewModel], result)

    async def get_schedule_detail(
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
            >>> async with AsyncActivitiesApi() as api:
            ...     # Option 1: Using config_id and date
            ...     detail = await api.get_schedule_detail(
            ...         config_id=123,
            ...         activity_date=datetime(2024, 12, 20)
            ...     )
            ...     # Option 2: Using session_id
            ...     detail = await api.get_schedule_detail(session_id=456)
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

        result = await self.api_client.call_api(
            resource_path=f"{self.base_path}/schedule/detail",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=AtividadeBasicoApiViewModel,
            auth_settings=["Basic"],
        )
        return cast(AtividadeBasicoApiViewModel, result)

    async def enroll(
        self,
        config_id: int,
        activity_date: datetime,
        member_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        slot_number: Optional[int] = None,
        origin: Optional[EOrigemAgendamento] = None,
    ) -> Any:
        """
        Enroll member or prospect in activity schedule.

        Args:
            config_id: Activity configuration ID
            activity_date: Activity schedule date
            member_id: Member ID (required if prospect_id not provided)
            prospect_id: Prospect ID (required if member_id not provided)
            slot_number: Slot number for spot booking
            origin: Enrollment origin

        Returns:
            Enrollment result

        Raises:
            ValueError: If neither member_id nor prospect_id provided

        Example:
            >>> async with AsyncActivitiesApi() as api:
            ...     # Enroll member
            ...     result = await api.enroll(
            ...         config_id=123,
            ...         activity_date=datetime(2024, 12, 20, 10, 0),
            ...         member_id=456,
            ...         slot_number=1
            ...     )
            ...     # Enroll prospect
            ...     result = await api.enroll(
            ...         config_id=123,
            ...         activity_date=datetime(2024, 12, 20, 10, 0),
            ...         prospect_id=789
            ...     )
        """
        if not (member_id or prospect_id):
            raise ValueError("Either member_id or prospect_id must be provided")

        params = {
            "idConfiguration": config_id,
            "activityDate": activity_date.isoformat(),
            "slotNumber": slot_number,
            "idMember": member_id,
            "idProspect": prospect_id,
            "origin": origin.value if origin is not None else None,
        }

        return await self.api_client.call_api(
            resource_path=f"{self.base_path}/schedule/enroll",
            method="POST",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
        )

    async def get_schedule(
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
            >>> async with AsyncActivitiesApi() as api:
            ...     schedule = await api.get_schedule(
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

        result = await self.api_client.call_api(
            resource_path=f"{self.base_path}/schedule",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[AtividadeAgendaApiViewModel],
            auth_settings=["Basic"],
        )
        return cast(List[AtividadeAgendaApiViewModel], result)

    async def create_experimental_class(
        self,
        prospect_id: int,
        activity_date: datetime,
        activity: str,
        service: str,
        activity_exists: bool = False,
        branch_id: Optional[int] = None,
    ) -> Any:
        """
        Create experimental class for prospect.

        Args:
            prospect_id: Prospect ID
            activity_date: Date for experimental class
            activity: Activity name
            service: Service name
            activity_exists: Whether activity already exists
            branch_id: Branch ID

        Returns:
            Experimental class creation result

        Example:
            >>> async with AsyncActivitiesApi() as api:
            ...     result = await api.create_experimental_class(
            ...         prospect_id=123,
            ...         activity_date=datetime(2024, 12, 20, 10, 0),
            ...         activity="Yoga",
            ...         service="Trial Class",
            ...         branch_id=1
            ...     )
        """
        params = {
            "idProspect": prospect_id,
            "activityDate": activity_date.isoformat(),
            "activity": activity,
            "service": service,
            "activityExists": activity_exists,
            "idBranch": branch_id,
        }

        return await self.api_client.call_api(
            resource_path=f"{self.base_path}/schedule/experimental-class",
            method="POST",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
        )

    async def change_status(
        self,
        status: EStatusAtividadeSessao,
        member_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        config_id: Optional[int] = None,
        activity_date: Optional[datetime] = None,
        session_id: Optional[int] = None,
    ) -> Any:
        """
        Change activity enrollment status.

        Args:
            status: New status for the activity enrollment
            member_id: Member ID
            prospect_id: Prospect ID
            config_id: Activity configuration ID
            activity_date: Activity date
            session_id: Activity session ID

        Returns:
            Status change result

        Example:
            >>> async with AsyncActivitiesApi() as api:
            ...     result = await api.change_status(
            ...         status=EStatusAtividadeSessao.PRESENTE,
            ...         member_id=123,
            ...         session_id=456
            ...     )
        """
        params = {
            "status": status.value,
            "idMember": member_id,
            "idProspect": prospect_id,
            "idConfiguration": config_id,
            "activityDate": activity_date.isoformat() if activity_date else None,
            "idActivitySession": session_id,
        }

        return await self.api_client.call_api(
            resource_path=f"{self.base_path}/schedule/enroll/change-status",
            method="POST",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
        )

    async def list_unavailable_spots(self, config_id: int, date: datetime) -> List[int]:
        """
        Get unavailable spots for activity configuration on specific date.

        Args:
            config_id: Activity configuration ID
            date: Date to check for unavailable spots

        Returns:
            List of unavailable spot numbers

        Example:
            >>> async with AsyncActivitiesApi() as api:
            ...     unavailable = await api.list_unavailable_spots(
            ...         config_id=123,
            ...         date=datetime(2024, 12, 20)
            ...     )
            ...     print(f"Unavailable spots: {unavailable}")
        """
        params = {
            "idConfiguration": config_id,
            "date": date.isoformat(),
        }

        result = await self.api_client.call_api(
            resource_path=f"{self.base_path}/list-unavailable-spots",
            method="GET",
            query_params=params,
            response_type=None,  # Returns list of integers directly
            auth_settings=["Basic"],
        )
        return cast(List[int], result)
