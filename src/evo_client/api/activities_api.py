from typing import Optional, List, Dict, Any, Union
from datetime import datetime

from ..core.api_client import ApiClient
from ..models.atividade_list_api_view_model import (
    AtividadeListApiViewModel,
)
from ..models.atividade_basico_api_view_model import (
    AtividadeBasicoApiViewModel,
)
from ..models.atividade_sessao_participante_api_view_model import (
    AtividadeSessaoParticipanteApiViewModel,
)
from ..models.e_status_atividade_sessao import EStatusAtividadeSessao
from ..models.e_origem_agendamento import EOrigemAgendamento


from typing import Optional, List, Dict, Any, Union, overload
from multiprocessing.pool import AsyncResult
from typing import Any


class ActivitiesApi:
    """Activities API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/activities"

    @overload
    def get_activities(
        self,
        search: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = True,
    ) -> AsyncResult[Any]: ...

    @overload
    def get_activities(
        self,
        search: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = False,
    ) -> List[AtividadeListApiViewModel]: ...

    def get_activities(
        self,
        search: Optional[str] = None,
        branch_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[List[AtividadeListApiViewModel], AsyncResult[Any]]:
        """
        Get activities list with optional filtering.

        Args:
            search: Filter by activity name, group name or tags
            branch_id: Filter by membership branch ID
            take: Number of records to return
            skip: Number of records to skip
            async_req: Execute request asynchronously
        """
        params = {"search": search, "idBranch": branch_id, "take": take, "skip": skip}

        return self.api_client.call_api(
            resource_path=f"{self.base_path}",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[AtividadeListApiViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def get_schedule_detail(
        self,
        config_id: Optional[int] = None,
        activity_date: Optional[datetime] = None,
        session_id: Optional[int] = None,
        async_req: bool = True,
    ) -> AsyncResult[Any]: ...

    @overload
    def get_schedule_detail(
        self,
        config_id: Optional[int] = None,
        activity_date: Optional[datetime] = None,
        session_id: Optional[int] = None,
        async_req: bool = False,
    ) -> AtividadeBasicoApiViewModel: ...

    def get_schedule_detail(
        self,
        config_id: Optional[int] = None,
        activity_date: Optional[datetime] = None,
        session_id: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[AtividadeBasicoApiViewModel, AsyncResult[Any]]:
        """
        Get activity schedule details.

        Args:
            config_id: Activity configuration ID (required with activity_date)
            activity_date: Activity date (required with config_id)
            session_id: Activity session ID (alternative to config_id/activity_date)
            async_req: Execute request asynchronously
        """
        if not ((config_id and activity_date) or session_id):
            raise ValueError(
                "Either provide both config_id and activity_date, or session_id"
            )

        params = {
            "idConfiguration": config_id,
            "activityDate": activity_date,
            "idActivitySession": session_id,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/schedule/detail",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=AtividadeBasicoApiViewModel,
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def enroll(
        self,
        config_id: int,
        activity_date: datetime,
        member_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        slot_number: Optional[int] = None,
        origin: Optional[EOrigemAgendamento] = None,
        async_req: bool = True,
    ) -> AsyncResult[Any]: ...

    @overload
    def enroll(
        self,
        config_id: int,
        activity_date: datetime,
        member_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        slot_number: Optional[int] = None,
        origin: Optional[EOrigemAgendamento] = None,
        async_req: bool = False,
    ) -> None: ...

    def enroll(
        self,
        config_id: int,
        activity_date: datetime,
        member_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        slot_number: Optional[int] = None,
        origin: Optional[EOrigemAgendamento] = None,
        async_req: bool = False,
    ) -> Union[None, AsyncResult[Any]]:
        """
        Enroll member or prospect in activity schedule.

        Args:
            config_id: Activity configuration ID
            activity_date: Activity schedule date
            member_id: Member ID (required if prospect_id not provided)
            prospect_id: Prospect ID (required if member_id not provided)
            slot_number: Slot number for spot booking
            origin: Enrollment origin
            async_req: Execute request asynchronously
        """
        if not (member_id or prospect_id):
            raise ValueError("Either member_id or prospect_id must be provided")

        params = {
            "idConfiguration": config_id,
            "activityDate": activity_date,
            "slotNumber": slot_number,
            "idMember": member_id,
            "idProspect": prospect_id,
            "origin": origin.value if origin else None,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/schedule/enroll",
            method="POST",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
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
        async_req: bool = True,
    ) -> AsyncResult[Any]: ...

    @overload
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
        async_req: bool = False,
    ) -> List[AtividadeSessaoParticipanteApiViewModel]: ...

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
        async_req: bool = False,
    ) -> Union[List[AtividadeSessaoParticipanteApiViewModel], AsyncResult[Any]]:
        """
        Get activities schedule with various filtering options.

        Status codes:
        - 0: Free
        - 1: Available
        - 2: Full
        - 3: Reservation Closed
        - 4: Restricted
        - 5: Registered
        - 6: Finished
        - 7: Cancelled
        - 8: In Queue
        - 10: Free Closed
        - 11: Restricted Closed
        - 12: Restricted Not Allowed
        - 15: Full No Waiting List
        """
        params = {
            "idMember": member_id,
            "date": date,
            "idBranch": branch_id,
            "idActivities": ",".join(map(str, activity_ids)) if activity_ids else None,
            "idAudiences": ",".join(map(str, audience_ids)) if audience_ids else None,
            "take": take,
            "onlyAvailables": only_availables,
            "showFullWeek": show_full_week,
            "idBranchToken": branch_token,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/schedule",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[AtividadeSessaoParticipanteApiViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def create_experimental_class(
        self,
        prospect_id: int,
        activity_date: datetime,
        activity: str,
        service: str,
        activity_exists: bool = False,
        branch_id: Optional[int] = None,
        async_req: bool = True,
    ) -> AsyncResult[Any]: ...

    @overload
    def create_experimental_class(
        self,
        prospect_id: int,
        activity_date: datetime,
        activity: str,
        service: str,
        activity_exists: bool = False,
        branch_id: Optional[int] = None,
        async_req: bool = False,
    ) -> None: ...

    def create_experimental_class(
        self,
        prospect_id: int,
        activity_date: datetime,
        activity: str,
        service: str,
        activity_exists: bool = False,
        branch_id: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[None, AsyncResult[Any]]:
        """Create a new experimental class and enroll the prospect."""
        params = {
            "idProspect": prospect_id,
            "activityDate": activity_date,
            "activity": activity,
            "service": service,
            "activityExist": activity_exists,
            "idBranch": branch_id,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/schedule/experimental-class",
            method="POST",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def change_status(
        self,
        status: EStatusAtividadeSessao,
        member_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        config_id: Optional[int] = None,
        activity_date: Optional[datetime] = None,
        session_id: Optional[int] = None,
        async_req: bool = True,
    ) -> AsyncResult[Any]: ...

    @overload
    def change_status(
        self,
        status: EStatusAtividadeSessao,
        member_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        config_id: Optional[int] = None,
        activity_date: Optional[datetime] = None,
        session_id: Optional[int] = None,
        async_req: bool = False,
    ) -> None: ...

    def change_status(
        self,
        status: EStatusAtividadeSessao,
        member_id: Optional[int] = None,
        prospect_id: Optional[int] = None,
        config_id: Optional[int] = None,
        activity_date: Optional[datetime] = None,
        session_id: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[None, AsyncResult[Any]]:
        """
        Change status of a member/prospect in activity schedule.

        Args:
            status: New status (0=Attending, 1=Absent, 2=Justified absence)
            member_id: Member ID
            prospect_id: Prospect ID
            config_id: Activity configuration ID (used with activity_date)
            activity_date: Activity date (used with config_id)
            session_id: Activity session ID (alternative to config_id/activity_date)
        """
        params = {
            "status": status.value,
            "idMember": member_id,
            "idProspect": prospect_id,
            "idConfiguration": config_id,
            "activityDate": activity_date,
            "idActivitySession": session_id,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/schedule/enroll/change-status",
            method="POST",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
            async_req=async_req,
        )

    @overload
    def get_unavailable_spots(
        self, config_id: int, date: datetime, async_req: bool = True
    ) -> AsyncResult[Any]: ...

    @overload
    def get_unavailable_spots(
        self, config_id: int, date: datetime, async_req: bool = False
    ) -> List[int]: ...

    def get_unavailable_spots(
        self, config_id: int, date: datetime, async_req: bool = False
    ) -> Union[List[int], AsyncResult[Any]]:
        """Get list of spots that are already filled in the activity session."""
        params = {"idConfiguration": config_id, "date": date}

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/list-unavailable-spots",
            method="GET",
            query_params=params,
            response_type=List[int],
            auth_settings=["Basic"],
            async_req=async_req,
        )
