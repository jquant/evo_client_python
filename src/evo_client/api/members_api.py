from typing import Optional, Union, Dict, Any, overload, List
from threading import Thread
from enum import Enum

from pydantic import BaseModel
from datetime import datetime

from ..core.api_client import ApiClient

from ..models.member_authenticate_view_model import MemberAuthenticateViewModel
from ..models.members_basic_api_view_model import MembersBasicApiViewModel
from ..models.member_data_view_model import MemberDataViewModel
from ..models.member_service_view_model import MemberServiceViewModel
from ..models.members_api_view_model import MembersApiViewModel


class Gender(str, Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "P"


class ContactType(int, Enum):
    TELEPHONE = 1
    CELLPHONE = 2


class MemberTransferViewModel(BaseModel):
    """Member transfer model."""

    # Define fields based on ClienteTransferenciaViewModel
    pass


class MembersApi:
    """Members API client for EVO API."""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()
        self.base_path = "/api/v1/members"

    @overload
    def authenticate_member(
        self,
        email: str,
        password: str,
        change_password: bool = False,
        async_req: bool = True,
    ) -> Thread: ...

    @overload
    def authenticate_member(
        self,
        email: str,
        password: str,
        change_password: bool = False,
        async_req: bool = False,
    ) -> MemberAuthenticateViewModel: ...

    def authenticate_member(
        self,
        email: str,
        password: str,
        change_password: bool = False,
        async_req: bool = False,
    ) -> Union[MemberAuthenticateViewModel, Thread]:
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
        async_req: bool = True,
    ) -> Thread: ...

    @overload
    def get_basic_info(
        self,
        email: Optional[str] = None,
        document: Optional[str] = None,
        phone: Optional[str] = None,
        member_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = False,
    ) -> MembersBasicApiViewModel: ...

    def get_basic_info(
        self,
        email: Optional[str] = None,
        document: Optional[str] = None,
        phone: Optional[str] = None,
        member_id: Optional[int] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[MembersBasicApiViewModel, Thread]:
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
    def get_fitcoins(self, id_member: int, async_req: bool = True) -> None: ...

    @overload
    def get_fitcoins(
        self, id_member: int, async_req: bool = False
    ) -> Union[None, Thread]: ...

    def get_fitcoins(
        self, id_member: int, async_req: bool = False
    ) -> Union[None, Thread]:
        pass

    @overload
    def update_fitcoins(
        self,
        id_member: int,
        fitcoin_type: str,
        fitcoin: int,
        reason: Optional[str] = None,
        async_req: bool = True,
    ) -> Thread: ...

    @overload
    def update_fitcoins(
        self,
        id_member: int,
        fitcoin_type: str,
        fitcoin: int,
        reason: Optional[str] = None,
        async_req: bool = False,
    ) -> None: ...

    def update_fitcoins(
        self,
        id_member: int,
        fitcoin_type: str,
        fitcoin: int,
        reason: Optional[str] = None,
        async_req: bool = False,
    ) -> Union[None, Thread]:
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
    def api_v1_members_fitcoins_put(
        self,
        id_member: Optional[int] = None,
        type: Optional[int] = None,
        fitcoin: Optional[int] = None,
        reason: Optional[str] = None,
        async_req: bool = True,
    ) -> Thread: ...

    @overload
    def api_v1_members_fitcoins_put(
        self,
        id_member: Optional[int] = None,
        type: Optional[int] = None,
        fitcoin: Optional[int] = None,
        reason: Optional[str] = None,
        async_req: bool = False,
    ) -> None: ...

    def api_v1_members_fitcoins_put(
        self,
        id_member: Optional[int] = None,
        type: Optional[int] = None,
        fitcoin: Optional[int] = None,
        reason: Optional[str] = None,
        async_req: bool = False,
    ) -> Union[None, Thread]:
        """Update a member fitcoins

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        Args:
            id_member: Id Member
            type: 1 - Add Fitcoins, 2 - Remove Fitcoins
            fitcoin: Quantity add/remove fitcoin
            reason: Reason add/remove fitcoin
            async_req: Execute request asynchronously

        Returns:
            None
            If async_req is True, returns the request thread
        """

        query_params = {
            "idMember": id_member,
            "type": type,
            "fitcoin": fitcoin,
            "reason": reason,
        }

        return self.api_client.call_api(
            resource_path=f"{self.base_path}/fitcoins",
            method="PUT",
            query_params=query_params,
            response_type=None,
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
        async_req: bool = False,
    ) -> Thread: ...

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
        async_req: bool = False,
    ) -> MemberDataViewModel: ...

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
    ) -> Union[MemberDataViewModel, Thread]:
        """
        Get members.

        Args:
            async_req: Execute request asynchronously

        Returns:
            Member data if synchronous, Thread if asynchronous
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
            response_type=MembersApiViewModel,
            auth_settings=["Basic"],
            async_req=async_req,
            headers={"Accept": "application/json"},
        )

    @overload
    def update_member_card(
        self, id_member: int, card_number: str, async_req: bool = True
    ) -> Thread: ...

    @overload
    def update_member_card(
        self, id_member: int, card_number: str, async_req: bool = False
    ) -> None: ...

    def update_member_card(
        self,
        id_member: int,
        card_number: str,
        async_req: bool = False,
    ) -> Union[None, Thread]:
        """
        Update a member card number.

        Args:
            id_member: Member ID to update card for
            card_number: New card number
            async_req: Execute request asynchronously

        Returns:
            None if synchronous, Thread if asynchronous
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
    def get_member_profile(self, id_member: int, async_req: bool = True) -> Thread: ...

    @overload
    def get_member_profile(
        self, id_member: int, async_req: bool = False
    ) -> MemberDataViewModel: ...

    def get_member_profile(
        self, id_member: int, async_req: bool = False
    ) -> Union[MemberDataViewModel, Thread]:
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
        async_req: bool = True,
    ) -> Thread: ...

    @overload
    def reset_password(
        self,
        user: str,
        sign_in: bool = False,
        async_req: bool = False,
    ) -> MemberAuthenticateViewModel: ...

    def reset_password(
        self,
        user: str,
        sign_in: bool = False,
        async_req: bool = False,
    ) -> Union[MemberAuthenticateViewModel, Thread]:
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
        async_req: bool = True,
    ) -> Thread: ...

    @overload
    def get_member_services(
        self,
        id_member: Optional[int] = None,
        async_req: bool = False,
    ) -> list: ...

    def get_member_services(
        self,
        id_member: Optional[int] = None,
        async_req: bool = False,
    ) -> Union[list, Thread]:
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
        self, transfer_data: MemberTransferViewModel, async_req: bool = True
    ) -> Thread: ...

    @overload
    def transfer_member(
        self, transfer_data: MemberTransferViewModel, async_req: bool = False
    ) -> None: ...

    def transfer_member(
        self, transfer_data: MemberTransferViewModel, async_req: bool = False
    ) -> Union[None, Thread]:
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
        async_req: bool = True,
    ) -> Thread: ...

    @overload
    def update_member_data(
        self,
        id_member: int,
        body: MemberDataViewModel,
        async_req: bool = False,
    ) -> bool: ...

    def update_member_data(
        self,
        id_member: int,
        body: MemberDataViewModel,
        async_req: bool = False,
    ) -> Union[bool, Thread]:
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
