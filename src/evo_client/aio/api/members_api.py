"""Async Members API client for EVO API."""

from typing import Optional

from ...models.members_basic_api_view_model import MembersBasicApiViewModel
from ...models.member_authenticate_view_model import MemberAuthenticateViewModel
from .base import AsyncBaseApi


class AsyncMembersApi(AsyncBaseApi):
    """Async Members API client for EVO API."""

    def __init__(self, api_client=None):
        """Initialize the async members API."""
        super().__init__(api_client)
        self.base_path = "/api/v1/members"

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
        Get basic member information with optional filtering.

        Args:
            email: Filter by email
            document: Filter by document
            phone: Filter by phone
            member_id: Filter by member ID
            take: Number of records to return (max 50)
            skip: Number of records to skip

        Returns:
            Member basic information

        Example:
            >>> async with AsyncMembersApi() as api:
            ...     info = await api.get_basic_info(email="user@example.com")
        """
        params = {
            "email": email,
            "document": document,
            "phone": phone,
            "idMember": member_id,
            "take": take,
            "skip": skip,
        }

        return await self.api_client.call_api(
            resource_path=f"{self.base_path}/basic-info",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=MembersBasicApiViewModel,
            auth_settings=["Basic"],
        )

    async def authenticate_member(
        self,
        email: str,
        password: str,
        change_password: bool = False,
    ) -> MemberAuthenticateViewModel:
        """
        Authenticate a member.

        Args:
            email: Member email
            password: Member password
            change_password: True if password needs to be changed

        Returns:
            Authentication result

        Example:
            >>> async with AsyncMembersApi() as api:
            ...     auth = await api.authenticate_member("user@example.com", "password")
        """
        params = {
            "email": email,
            "password": password,
            "changePassword": change_password,
        }

        return await self.api_client.call_api(
            resource_path=f"{self.base_path}/auth",
            method="POST",
            query_params=params,
            response_type=MemberAuthenticateViewModel,
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )

    async def update_fitcoins(
        self,
        id_member: int,
        fitcoin_type: str,
        fitcoin: int,
        reason: Optional[str] = None,
    ) -> bool:
        """
        Update member fitcoins.

        Args:
            id_member: Member ID to update fitcoins
            fitcoin_type: Type of fitcoin operation
            fitcoin: Number of fitcoins
            reason: Reason for the update

        Returns:
            True if successful

        Example:
            >>> async with AsyncMembersApi() as api:
            ...     success = await api.update_fitcoins(123, "add", 100, "Bonus reward")
        """
        params = {
            "idMember": id_member,
            "type": fitcoin_type,
            "fitcoin": fitcoin,
            "reason": reason,
        }

        response = await self.api_client.call_api(
            resource_path=f"{self.base_path}/fitcoins",
            method="PUT",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
            headers={"Accept": "application/json"},
        )

        # Return True for successful response
        return response is not None
