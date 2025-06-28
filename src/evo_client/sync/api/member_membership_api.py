"""Clean synchronous Member Membership API."""

from datetime import datetime
from typing import Any, List, Optional, cast

from ...models.contratos_cancelados_resumo_api_view_model import (
    ContratosCanceladosResumoApiViewModel,
)
from ...models.member_membership_api_view_model import MemberMembershipApiViewModel
from .base import SyncBaseApi


class SyncMemberMembershipApi(SyncBaseApi):
    """Clean synchronous Member Membership API client."""

    def __init__(self, api_client=None):
        super().__init__(api_client)
        self.base_path_v1 = "/api/v1/membermembership"
        self.base_path_v2 = "/api/v2/membermembership"

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
    ) -> Any:
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

        Returns:
            Cancellation result

        Example:
            >>> with SyncMemberMembershipApi() as api:
            ...     result = api.cancel_membership(
            ...         id_member_membership=123,
            ...         id_member_branch=1,
            ...         cancellation_date=datetime.now(),
            ...         reason_cancellation="Member requested",
            ...         cancel_future_releases=True
            ...     )
            ...     print(f"Membership cancelled: {result}")
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

        result = self.api_client.call_api(
            resource_path=f"{self.base_path_v1}/cancellation",
            method="POST",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return result

    def get_membership(self, id_member_membership: int) -> MemberMembershipApiViewModel:
        """
        Get membership details by ID.

        Args:
            id_member_membership: Membership ID

        Returns:
            Membership details

        Example:
            >>> with SyncMemberMembershipApi() as api:
            ...     membership = api.get_membership(id_member_membership=123)
            ...     print(f"Membership: {membership.member_name} - {membership.membership_name}")
        """
        result = self.api_client.call_api(
            resource_path=f"{self.base_path_v1}/{id_member_membership}",
            method="GET",
            response_type=MemberMembershipApiViewModel,
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return cast(MemberMembershipApiViewModel, result)

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
    ) -> List[ContratosCanceladosResumoApiViewModel]:
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

        Returns:
            List of canceled membership summaries

        Raises:
            ValueError: If take > 25

        Example:
            >>> with SyncMemberMembershipApi() as api:
            ...     canceled = api.get_canceled_memberships(
            ...         cancel_date_start=datetime(2024, 1, 1),
            ...         cancel_date_end=datetime(2024, 12, 31),
            ...         take=10
            ...     )
            ...     for membership in canceled:
            ...         print(f"Canceled: {membership.member_name} - {membership.reason}")
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

        result = self.api_client.call_api(
            resource_path=f"{self.base_path_v2}",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[ContratosCanceladosResumoApiViewModel],
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return cast(List[ContratosCanceladosResumoApiViewModel], result)
