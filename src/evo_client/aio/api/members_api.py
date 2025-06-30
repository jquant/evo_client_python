"""Async Members API client for EVO API."""

from datetime import datetime
from typing import Any, List, Optional, cast

from ...models.cliente_detalhes_basicos_api_view_model import (
    ClienteDetalhesBasicosApiViewModel,
)
from ...models.member_authenticate_view_model import MemberAuthenticateViewModel
from ...models.member_data_view_model import MemberDataViewModel
from ...models.member_transfer_view_model import MemberTransferViewModel
from ...models.members_api_view_model import MembersApiViewModel
from ...models.members_basic_api_view_model import MembersBasicApiViewModel
from .base import AsyncBaseApi


class AsyncMembersApi(AsyncBaseApi):
    """Async Members API client for EVO API."""

    def __init__(self, api_client=None):
        """Initialize the async members API."""
        super().__init__(api_client)
        self.base_path = "/api/v1/members"
        self.base_path_v2 = "/api/v2/members"

    async def authenticate_member(
        self,
        email: str,
        password: str,
        change_password: bool = False,
    ) -> MemberAuthenticateViewModel:
        """
        Authenticate member.

        Args:
            email: Member email
            password: Member password
            change_password: True if password needs to be changed

        Returns:
            Member authentication details

        Example:
            >>> async with AsyncMembersApi() as api:
            ...     result = await api.authenticate_member("user@example.com", "password123")
            ...     print(result.authenticated)
        """
        params = {
            "email": email,
            "password": password,
            "changePassword": change_password,
        }

        result = await self.api_client.call_api(
            resource_path=f"{self.base_path}/auth",
            method="POST",
            query_params=params,
            response_type=MemberAuthenticateViewModel,
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return cast(MemberAuthenticateViewModel, result)

    async def get_basic_info(
        self,
        email: Optional[str] = None,
        document: Optional[str] = None,
        phone: Optional[str] = None,
        member_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
    ) -> MembersBasicApiViewModel:
        """
        Get basic member information.

        Args:
            email: Filter by member email
            document: Filter by member document
            phone: Filter by phone (format: 1112341234)
            member_id: Filter by member ID
            take: Number of records to return (max 50)
            skip: Number of records to skip

        Returns:
            Basic member information

        Raises:
            ValueError: If take > 50

        Example:
            >>> async with AsyncMembersApi() as api:
            ...     result = await api.get_basic_info(email="user@example.com")
            ...     print(result.data[0].name if result.data else "No member found")
        """
        if take and take > 50:
            raise ValueError("Maximum number of records to return is 50")

        params = {
            "email": email,
            "document": document,
            "phone": phone,
            "idMember": member_id,
            "take": take,
            "skip": skip,
        }

        result = await self.api_client.call_api(
            resource_path=f"{self.base_path}/basic",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=MembersBasicApiViewModel,
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return cast(MembersBasicApiViewModel, result)

    async def update_fitcoins(
        self,
        id_member: int,
        fitcoin_type: str,
        fitcoin: int,
        reason: Optional[str] = None,
    ) -> Any:
        """
        Update member fitcoins.

        Args:
            id_member: Member ID to update fitcoins
            fitcoin_type: Type of fitcoin operation ("add" or "subtract")
            fitcoin: Amount of fitcoins to add/subtract
            reason: Reason for the fitcoin update

        Returns:
            Update result

        Example:
            >>> async with AsyncMembersApi() as api:
            ...     result = await api.update_fitcoins(123, "add", 100, "Bonus points")
        """
        params = {
            "idMember": id_member,
            "fitcoinType": fitcoin_type,
            "fitcoin": fitcoin,
            "reason": reason,
        }

        return await self.api_client.call_api(
            resource_path=f"{self.base_path}/fitcoins",
            method="PUT",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=None,
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )

    async def get_members(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        document: Optional[str] = None,
        phone: Optional[str] = None,
        conversion_date_start: Optional[datetime] = None,
        conversion_date_end: Optional[datetime] = None,
        register_date_start: Optional[datetime] = None,
        register_date_end: Optional[datetime] = None,
        membership_start_date_start: Optional[datetime] = None,
        membership_start_date_end: Optional[datetime] = None,
        membership_cancel_date_start: Optional[datetime] = None,
        membership_cancel_date_end: Optional[datetime] = None,
        status: Optional[int] = None,
        token_gympass: Optional[str] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        ids_members: Optional[str] = None,
        only_personal: bool = False,
        personal_type: Optional[int] = None,
        show_activity_data: bool = False,
    ) -> List[MembersApiViewModel]:
        """
        Get members list with filtering options.

        Args:
            name: Filter by member name
            email: Filter by member email
            document: Filter by member document
            phone: Filter by phone (format: 1112341234)
            conversion_date_start: Filter by conversion date from
            conversion_date_end: Filter by conversion date to
            register_date_start: Filter by registration date from
            register_date_end: Filter by registration date to
            membership_start_date_start: Filter by membership start date from
            membership_start_date_end: Filter by membership start date to
            membership_cancel_date_start: Filter by membership cancel date from
            membership_cancel_date_end: Filter by membership cancel date to
            status: Filter by member status (1=Active, 2=Inactive)
            token_gympass: Filter by gympass token
            take: Number of records to return (max 50)
            skip: Number of records to skip
            ids_members: Filter by member IDs (comma-separated: "1,2,3")
            only_personal: Show only personal trainers
            personal_type: Filter by personal type (1=Internal, 2=External)
            show_activity_data: Include activity data

        Returns:
            List of members matching the criteria

        Raises:
            ValueError: If take > 50

        Example:
            >>> async with AsyncMembersApi() as api:
            ...     members = await api.get_members(name="John", take=10)
            ...     for member in members:
            ...         print(f"{member.name} - {member.email}")
        """
        if take and take > 50:
            raise ValueError("Maximum number of records to return is 50")

        params = {
            "name": name,
            "email": email,
            "document": document,
            "phone": phone,
            "conversionDateStart": (
                conversion_date_start.isoformat() if conversion_date_start else None
            ),
            "conversionDateEnd": (
                conversion_date_end.isoformat() if conversion_date_end else None
            ),
            "registerDateStart": (
                register_date_start.isoformat() if register_date_start else None
            ),
            "registerDateEnd": (
                register_date_end.isoformat() if register_date_end else None
            ),
            "membershipStartDateStart": (
                membership_start_date_start.isoformat()
                if membership_start_date_start
                else None
            ),
            "membershipStartDateEnd": (
                membership_start_date_end.isoformat()
                if membership_start_date_end
                else None
            ),
            "membershipCancelDateStart": (
                membership_cancel_date_start.isoformat()
                if membership_cancel_date_start
                else None
            ),
            "membershipCancelDateEnd": (
                membership_cancel_date_end.isoformat()
                if membership_cancel_date_end
                else None
            ),
            "status": status,
            "tokenGympass": token_gympass,
            "take": take,
            "skip": skip,
            "idsMembers": ids_members,
            "onlyPersonal": only_personal,
            "personalType": personal_type,
            "showActivityData": show_activity_data,
        }

        result = await self.api_client.call_api(
            resource_path=self.base_path_v2,
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=List[MembersApiViewModel],
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return cast(List[MembersApiViewModel], result)

    async def update_member_card(self, id_member: int, card_number: str) -> Any:
        """
        Update member card number.

        Args:
            id_member: Member ID to update card for
            card_number: New card number

        Returns:
            Update result

        Example:
            >>> async with AsyncMembersApi() as api:
            ...     result = await api.update_member_card(123, "1234567890")
        """
        params = {
            "idMember": id_member,
            "cardNumber": card_number,
        }

        return await self.api_client.call_api(
            resource_path=f"{self.base_path}/{id_member}/card",
            method="PUT",
            query_params=params,
            response_type=None,
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )

    async def get_member_profile(
        self, id_member: int
    ) -> ClienteDetalhesBasicosApiViewModel:
        """
        Get detailed member profile.

        Args:
            id_member: Member ID to get profile for

        Returns:
            Detailed member profile information

        Example:
            >>> async with AsyncMembersApi() as api:
            ...     profile = await api.get_member_profile(123)
            ...     print(f"Member: {profile.name} - {profile.email}")
        """
        result = await self.api_client.call_api(
            resource_path=f"{self.base_path_v2}/{id_member}",
            method="GET",
            response_type=ClienteDetalhesBasicosApiViewModel,
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return cast(ClienteDetalhesBasicosApiViewModel, result)

    async def reset_password(
        self, user: str, sign_in: bool = False
    ) -> MemberAuthenticateViewModel:
        """
        Reset member password.

        Args:
            user: Member username or email
            sign_in: True to sign in after reset

        Returns:
            Password reset result with authentication details

        Example:
            >>> async with AsyncMembersApi() as api:
            ...     result = await api.reset_password("user@example.com", True)
            ...     print(f"Password reset: {result.success}")
        """
        params = {
            "user": user,
            "signIn": sign_in,
        }

        result = await self.api_client.call_api(
            resource_path=f"{self.base_path}/resetPassword",
            method="POST",
            query_params=params,
            response_type=MemberAuthenticateViewModel,
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return cast(MemberAuthenticateViewModel, result)

    async def get_member_services(self, id_member: Optional[int] = None) -> list:
        """
        Get services available for member.

        Args:
            id_member: Member ID to get services for (optional)

        Returns:
            List of available services for the member

        Example:
            >>> async with AsyncMembersApi() as api:
            ...     services = await api.get_member_services(123)
            ...     for service in services:
            ...         print(f"Service: {service}")
        """
        params = {}
        if id_member:
            params["idMember"] = id_member

        result = await self.api_client.call_api(
            resource_path=f"{self.base_path}/services",
            method="GET",
            query_params=params if params else None,
            response_type=list,
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
        return cast(list, result)

    async def transfer_member(self, transfer_data: MemberTransferViewModel) -> Any:
        """
        Transfer member to another branch.

        Args:
            transfer_data: Transfer details including member ID, target branch, etc.

        Returns:
            Transfer result

        Example:
            >>> async with AsyncMembersApi() as api:
            ...     transfer = MemberTransferViewModel(...)
            ...     result = await api.transfer_member(transfer)
        """
        return await self.api_client.call_api(
            resource_path=f"{self.base_path}/transfer",
            method="POST",
            body=transfer_data.model_dump(exclude_unset=True, by_alias=True),
            response_type=None,
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )

    async def update_member_data(
        self, id_member: int, body: MemberDataViewModel
    ) -> Any:
        """
        Update member data.

        Args:
            id_member: Member ID to update
            body: Updated member data

        Returns:
            Update result

        Example:
            >>> async with AsyncMembersApi() as api:
            ...     member_data = MemberDataViewModel(...)
            ...     result = await api.update_member_data(123, member_data)
        """
        return await self.api_client.call_api(
            resource_path=f"{self.base_path}/update-member-data/{id_member}",
            method="PUT",
            body=body.model_dump(exclude_unset=True, by_alias=True),
            response_type=None,
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )
