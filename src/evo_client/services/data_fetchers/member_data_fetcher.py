from typing import List, Optional, Dict
from datetime import datetime

from evo_client.models.members_api_view_model import MembersApiViewModel
from evo_client.api.members_api import MembersApi
from evo_client.core.api_client import ApiClient
from evo_client.utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher


class MemberDataFetcher(BaseDataFetcher):
    """Handles fetching and processing member-related data."""
    
    def __init__(self, members_api: MembersApi, branch_api_clients: Optional[Dict[str, ApiClient]] = None):
        super().__init__(members_api, branch_api_clients)
    
    def fetch_member_by_id(self, member_id: str) -> Optional[MembersApiViewModel]:
        """Fetch a specific member by their ID."""
        result = self.api.get_member_profile(id_member=int(member_id))
        return result
    
    def fetch_members(
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
        ids_members: Optional[str] = None,
        only_personal: bool = False,
        personal_type: Optional[int] = None,
        show_activity_data: bool = False
    ) -> List[MembersApiViewModel]:
        """Fetch members with various filters."""
        return paginated_api_call(
            api_func=self.api.get_members,
            parallel_units=self.branch_ids,
            name=name,
            email=email,
            document=document,
            phone=phone,
            conversion_date_start=conversion_date_start,
            conversion_date_end=conversion_date_end,
            register_date_start=register_date_start,
            register_date_end=register_date_end,
            membership_start_date_start=membership_start_date_start,
            membership_start_date_end=membership_start_date_end,
            membership_cancel_date_start=membership_cancel_date_start,
            membership_cancel_date_end=membership_cancel_date_end,
            status=status,
            token_gympass=token_gympass,
            ids_members=ids_members,
            only_personal=only_personal,
            personal_type=personal_type,
            show_activity_data=show_activity_data,
        )
    