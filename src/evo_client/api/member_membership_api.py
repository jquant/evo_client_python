from typing import List, Optional, Union, overload
from datetime import datetime
from threading import Thread

from pydantic import BaseModel

from ..core.api_client import ApiClient
from ..models.contratos_cancelados_resumo_api_view_model import (
    ContratosCanceladosResumoApiViewModel,
)
from ..models.member_membership_api_view_model import MemberMembershipApiViewModel


class MemberMembershipApi:
    """Member Membership API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/membermembership"

    @overload
    def cancel_membership(
        self,
        id_member_membership: int,
        id_member_branch: int,
        cancellation_date: datetime,
        reason_cancellation: str,
        notice_cancellation: Optional[str] = None,
        cancel_future_releases: bool = False,
        cancel_future_sessions: bool = False,
        convert_credit_days: bool = False,
        schedule_cancellation: bool = False,
        schedule_cancellation_date: Optional[datetime] = None,
        add_fine: bool = False,
        value_fine: Optional[float] = None,
        async_req: bool = True,
    ) -> Thread: ...

    @overload
    def cancel_membership(
        self,
        id_member_membership: int,
        id_member_branch: int,
        cancellation_date: datetime,
        reason_cancellation: str,
        notice_cancellation: Optional[str] = None,
        cancel_future_releases: bool = False,
        cancel_future_sessions: bool = False,
        convert_credit_days: bool = False,
        schedule_cancellation: bool = False,
        schedule_cancellation_date: Optional[datetime] = None,
        add_fine: bool = False,
        value_fine: Optional[float] = None,
        async_req: bool = False,
    ) -> None: ...

    def cancel_membership(
        self,
        id_member_membership: int,
        id_member_branch: int,
        cancellation_date: datetime,
        reason_cancellation: str,
        notice_cancellation: Optional[str] = None,
        cancel_future_releases: bool = False,
        cancel_future_sessions: bool = False,
        convert_credit_days: bool = False,
        schedule_cancellation: bool = False,
        schedule_cancellation_date: Optional[datetime] = None,
        add_fine: bool = False,
        value_fine: Optional[float] = None,
        async_req: bool = False,
    ) -> Union[None, Thread]:
        """
        Cancel member membership.

        Args:
            id_member_membership: ID of membership to cancel
            id_member_branch: Branch ID where cancellation occurs
            cancellation_date: Date of cancellation
            reason_cancellation: Reason for cancellation
            notice_cancellation: Additional notes
            cancel_future_releases: Cancel all future releases
            cancel_future_sessions: Cancel all future sessions
            convert_credit_days: Convert remaining credits to days
            schedule_cancellation: Schedule future cancellation
            schedule_cancellation_date: Future cancellation date
            add_fine: Apply cancellation fine
            value_fine: Fine amount
            async_req: Execute request asynchronously
        """
        params = {
            "IdMemberMembership": id_member_membership,
            "IdMemberBranch": id_member_branch,
            "CancellationDate": cancellation_date,
            "ReasonCancellation": reason_cancellation,
            "NoticeCancellation": notice_cancellation,
            "CancelFutureReleases": cancel_future_releases,
            "CancelFutureSessions": cancel_future_sessions,
            "ConvertCreditDays": convert_credit_days,
            "ScheduleCancellation": schedule_cancellation,
            "ScheduleCancellationDate": schedule_cancellation_date,
            "AddFine": add_fine,
            "ValueFine": value_fine,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/cancellation",
            method="POST",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def get_membership(
        self, id_member_membership: int, async_req: bool = True
    ) -> MemberMembershipApiViewModel: ...

    @overload
    def get_membership(
        self, id_member_membership: int, async_req: bool = False
    ) -> MemberMembershipApiViewModel: ...

    def get_membership(
        self, id_member_membership: int, async_req: bool = False
    ) -> Union[MemberMembershipApiViewModel, Thread]:
        """
        Get membership details by ID.

        Args:
            id_member_membership: Membership ID
            async_req: Execute request asynchronously
        """
        return self.api_client.call_api(
            resource_path=f"{self.base_path}/{id_member_membership}",
            method="GET",
            response_type=MemberMembershipApiViewModel,
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def get_canceled_memberships(
        self,
        id_member: Optional[int] = None,
        id_membership: Optional[int] = None,
        member_name: Optional[str] = None,
        register_date_start: Optional[datetime] = None,
        register_date_end: Optional[datetime] = None,
        cancel_date_start: Optional[datetime] = None,
        cancel_date_end: Optional[datetime] = None,
        show_transfers: bool = False,
        show_aggregators: bool = False,
        show_vips: bool = False,
        contract_type: Optional[str] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = True,
    ) -> List[ContratosCanceladosResumoApiViewModel]: ...

    @overload
    def get_canceled_memberships(
        self,
        id_member: Optional[int] = None,
        id_membership: Optional[int] = None,
        member_name: Optional[str] = None,
        register_date_start: Optional[datetime] = None,
        register_date_end: Optional[datetime] = None,
        cancel_date_start: Optional[datetime] = None,
        cancel_date_end: Optional[datetime] = None,
        show_transfers: bool = False,
        show_aggregators: bool = False,
        show_vips: bool = False,
        contract_type: Optional[str] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = False,
    ) -> List[ContratosCanceladosResumoApiViewModel]: ...

    def get_canceled_memberships(
        self,
        id_member: Optional[int] = None,
        id_membership: Optional[int] = None,
        member_name: Optional[str] = None,
        register_date_start: Optional[datetime] = None,
        register_date_end: Optional[datetime] = None,
        cancel_date_start: Optional[datetime] = None,
        cancel_date_end: Optional[datetime] = None,
        show_transfers: bool = False,
        show_aggregators: bool = False,
        show_vips: bool = False,
        contract_type: Optional[str] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[List[ContratosCanceladosResumoApiViewModel], Thread]:
        """
        Get summary of canceled memberships.

        Args:
            id_member: Filter by member ID
            id_membership: Filter by membership ID
            member_name: Filter by member name
            register_date_start: Filter by registration start date
            register_date_end: Filter by registration end date
            cancel_date_start: Filter by cancellation start date
            cancel_date_end: Filter by cancellation end date
            show_transfers: Include transferred contracts
            show_aggregators: Include aggregator contracts
            show_vips: Include VIP contracts
            contract_type: Filter by contract types (comma-separated)
            take: Number of records to return (max 25)
            skip: Number of records to skip
            async_req: Execute request asynchronously

        Raises:
            ValueError: If take > 25
        """
        if take and take > 25:
            raise ValueError("Maximum number of records to return is 25")

        params = {
            "idMember": id_member,
            "idMembership": id_membership,
            "memberName": member_name,
            "registerDateStart": register_date_start,
            "registerDateEnd": register_date_end,
            "cancelDateStart": cancel_date_start,
            "cancelDateEnd": cancel_date_end,
            "showTransfers": show_transfers,
            "showAggregators": show_aggregators,
            "showVips": show_vips,
            "contractType": contract_type,
            "take": take,
            "skip": skip,
        }

        return self.api_client.call_api(
            resource_path="/api/v2/membermembership",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[ContratosCanceladosResumoApiViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )
