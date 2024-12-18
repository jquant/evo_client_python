from datetime import datetime
from multiprocessing.pool import AsyncResult
from typing import Any, List, Literal, Optional, Union, overload

from .base import BaseApi
from ..core.api_client import ApiClient
from ..models.cliente_detalhes_basicos_api_view_model import (
    ClienteDetalhesBasicosApiViewModel,
)
from ..models.member_authenticate_view_model import MemberAuthenticateViewModel
from ..models.member_data_view_model import MemberDataViewModel
from ..models.members_api_view_model import MembersApiViewModel
from ..models.member_service_view_model import MemberServiceViewModel
from ..models.member_transfer_view_model import MemberTransferViewModel
from ..models.members_basic_api_view_model import MembersBasicApiViewModel


class MembersApi(BaseApi):
    """Members API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        super().__init__(api_client)
        self.base_path = "/api/v1/members"

    @overload
    def authenticate_member(
        self,
        email: str,
        password: str,
        change_password: bool = False,
        async_req: Literal[False] = False,
    ) -> MemberAuthenticateViewModel: ...

    @overload
    def authenticate_member(
        self,
        email: str,
        password: str,
        change_password: bool = False,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    def authenticate_member(
        self,
        email: str,
        password: str,
        change_password: bool = False,
        async_req: bool = False,
    ) -> Union[MemberAuthenticateViewModel, AsyncResult[Any]]:
        """
        Authenticate member.

        Args:
            email: Member email
            password: Member password
            change_password: True if password needs to be changed
            async_req: Execute request asynchronously
        """
        params = {
            "email": email,
            "password": password,
            "changePassword": change_password,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/auth",
            method="POST",
            query_params=params,
            response_type=MemberAuthenticateViewModel,
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def get_basic_info(
        self,
        email: Optional[str] = None,
        document: Optional[str] = None,
        phone: Optional[str] = None,
        member_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: Literal[False] = False,
    ) -> MembersBasicApiViewModel: ...

    @overload
    def get_basic_info(
        self,
        email: Optional[str] = None,
        document: Optional[str] = None,
        phone: Optional[str] = None,
        member_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    def get_basic_info(
        self,
        email: Optional[str] = None,
        document: Optional[str] = None,
        phone: Optional[str] = None,
        member_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[MembersBasicApiViewModel, AsyncResult[Any]]:
        """
        Get basic member information.

        Args:
            email: Filter by member email
            document: Filter by member document
            phone: Filter by phone (format: 1112341234)
            member_id: Filter by member ID
            take: Number of records to return (max 50)
            skip: Number of records to skip
            async_req: Execute request asynchronously

        Raises:
            ValueError: If take > 50
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

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/basic",
            method="GET",
            query_params={k: v for k, v in params.items() if v is not None},
            response_type=MembersBasicApiViewModel,
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def get_fitcoins(
        self, id_member: int, async_req: Literal[False] = False
    ) -> Union[None, AsyncResult[Any]]: ...

    @overload
    def get_fitcoins(self, id_member: int, async_req: Literal[True] = True) -> None: ...

    def get_fitcoins(
        self, id_member: int, async_req: bool = False
    ) -> Union[None, AsyncResult[Any]]:
        raise NotImplementedError("Not implemented")

    @overload
    def update_fitcoins(
        self,
        id_member: int,
        fitcoin_type: str,
        fitcoin: int,
        reason: Optional[str] = None,
        async_req: Literal[False] = False,
    ) -> Any: ...

    @overload
    def update_fitcoins(
        self,
        id_member: int,
        fitcoin_type: str,
        fitcoin: int,
        reason: Optional[str] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    def update_fitcoins(
        self,
        id_member: int,
        fitcoin_type: str,
        fitcoin: int,
        reason: Optional[str] = None,
        async_req: bool = False,
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Update member fitcoins.

        Args:
            member_id: Member ID to update fitcoins
            fitcoin_type: Type of fitcoin operation
            fitcoins: Number of fitcoins
            reason: Reason for the update
            async_req: Execute request asynchronously
        """
        params = {
            "idMember": id_member,
            "type": fitcoin_type,
            "fitcoin": fitcoin,
            "reason": reason,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/fitcoins",
            method="PUT",
            query_params={k: v for k, v in params.items() if v is not None},
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def get_members(
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
        async_req: Literal[False] = False,
    ) -> List[MembersApiViewModel]: ...

    @overload
    def get_members(
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
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    def get_members(
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
        async_req: bool = False,
    ) -> Union[List[MembersApiViewModel], AsyncResult[Any]]:
        """
        Get members.

        Args:
            async_req: Execute request asynchronously

        Returns:
            Member data if synchronous, AsyncResult[Any] if asynchronous
        """
        query_params = {
            "name": name,
            "email": email,
            "document": document,
            "phone": phone,
            "conversionDateStart": conversion_date_start,
            "conversionDateEnd": conversion_date_end,
            "registerDateStart": register_date_start,
            "registerDateEnd": register_date_end,
            "membershipStartDateStart": membership_start_date_start,
            "membershipStartDateEnd": membership_start_date_end,
            "membershipCancelDateStart": membership_cancel_date_start,
            "membershipCancelDateEnd": membership_cancel_date_end,
            "status": status,
            "tokenGympass": token_gympass,
            "take": take,
            "skip": skip,
            "idsMembers": ids_members,
            "onlyPersonal": only_personal,
            "personalType": personal_type,
            "showActivityData": show_activity_data,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}",
            method="GET",
            query_params=query_params,
            response_type=List[MembersApiViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def update_member_card(
        self, id_member: int, card_number: str, async_req: Literal[False] = False
    ) -> Any: ...

    @overload
    def update_member_card(
        self, id_member: int, card_number: str, async_req: Literal[True] = True
    ) -> AsyncResult[Any]: ...

    def update_member_card(
        self,
        id_member: int,
        card_number: str,
        async_req: bool = False,
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Update a member card number.

        Args:
            id_member: Member ID to update card for
            card_number: New card number
            async_req: Execute request asynchronously

        Returns:
            None if synchronous, AsyncResult[Any] if asynchronous
        """
        query_params = {"cardNumber": card_number}

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/{id_member}/card",
            method="PUT",
            query_params=query_params,
            response_type=None,
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def get_member_profile(
        self, id_member: int, async_req: Literal[False] = False
    ) -> ClienteDetalhesBasicosApiViewModel: ...

    @overload
    def get_member_profile(
        self, id_member: int, async_req: Literal[True] = True
    ) -> AsyncResult[Any]: ...

    def get_member_profile(
        self, id_member: int, async_req: bool = False
    ) -> Union[ClienteDetalhesBasicosApiViewModel, AsyncResult[Any]]:
        """
        Get member profile.

        Args:
            id_member: Member ID to get profile for
            async_req: Execute request asynchronously
        """
        return self.api_client.call_api(
            resource_path=f"{self.base_path}/{id_member}",
            method="GET",
            response_type=MemberDataViewModel,
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def reset_password(
        self,
        user: str,
        sign_in: bool = False,
        async_req: Literal[False] = False,
    ) -> MemberAuthenticateViewModel: ...

    @overload
    def reset_password(
        self,
        user: str,
        sign_in: bool = False,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    def reset_password(
        self,
        user: str,
        sign_in: bool = False,
        async_req: bool = False,
    ) -> Union[MemberAuthenticateViewModel, AsyncResult[Any]]:
        """
        Get link for reset password.

        Args:
            user: Filter by CPF, idMember or e-mail
            sign_in: Check true if after change password you want sign in
            async_req: Execute request asynchronously
        """
        params = {
            "user": user,
            "signIn": sign_in,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/resetPassword",
            method="GET",
            query_params=params,
            response_type=MemberAuthenticateViewModel,
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def get_member_services(
        self,
        id_member: Optional[int] = None,
        async_req: Literal[False] = False,
    ) -> list: ...

    @overload
    def get_member_services(
        self,
        id_member: Optional[int] = None,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    def get_member_services(
        self,
        id_member: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[list, AsyncResult[Any]]:
        """
        Get member services.

        Args:
            id_member: Filter by member id
            async_req: Execute request asynchronously
        """
        params = {}
        if id_member is not None:
            params["idMember"] = id_member

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/services",
            method="GET",
            query_params=params,
            response_type=List[MemberServiceViewModel],
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def transfer_member(
        self, transfer_data: MemberTransferViewModel, async_req: Literal[False] = False
    ) -> Any: ...

    @overload
    def transfer_member(
        self, transfer_data: MemberTransferViewModel, async_req: Literal[True] = True
    ) -> AsyncResult[Any]: ...

    def transfer_member(
        self, transfer_data: MemberTransferViewModel, async_req: bool = False
    ) -> Union[Any, AsyncResult[Any]]:
        """
        Transfer member to another branch/unit.

        Args:
            transfer_data: Transfer details
            async_req: Execute request asynchronously
        """
        return self.api_client.call_api(
            resource_path=f"{self.base_path}/transfer",
            method="POST",
            body=transfer_data.model_dump(exclude_unset=True),
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )

    @overload
    def update_member_data(
        self,
        id_member: int,
        body: MemberDataViewModel,
        async_req: Literal[False] = False,
    ) -> bool: ...

    @overload
    def update_member_data(
        self,
        id_member: int,
        body: MemberDataViewModel,
        async_req: Literal[True] = True,
    ) -> AsyncResult[Any]: ...

    def update_member_data(
        self,
        id_member: int,
        body: MemberDataViewModel,
        async_req: bool = False,
    ) -> Union[bool, AsyncResult[Any]]:
        """
        Update basic member data.

        Args:
            id_member: Member ID
            body: Member data to update
            async_req: Execute request asynchronously

        Returns:
            True if successful, False otherwise
        """
        params = {}
        if id_member is not None:
            params["idMember"] = id_member

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/update-member-data/{id_member}",
            method="PATCH",
            body=body,
            response_type=bool,
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
