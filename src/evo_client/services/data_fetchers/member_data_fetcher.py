from typing import List, Optional
from datetime import datetime
from loguru import logger

from ...api.members_api import MembersApi
from ...models.cliente_detalhes_basicos_api_view_model import (
    ClienteDetalhesBasicosApiViewModel,
)
from ...models.members_api_view_model import MembersApiViewModel
from ...utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher


class MemberDataFetcher(BaseDataFetcher):
    """Handles fetching and processing member-related data."""

    def fetch_member_by_id(
        self, member_id: str, branch_id: Optional[int] = None
    ) -> Optional[ClienteDetalhesBasicosApiViewModel]:
        """Fetch a specific member by their ID.

        Args:
            member_id: The ID of the member to fetch

        Returns:
            Optional[MembersApiViewModel]: The member data if found, None otherwise
        """
        try:
            if branch_id and branch_id in self.get_available_branch_ids():
                branch_api = MembersApi(api_client=self.get_branch_api(branch_id))
                if branch_api:
                    result = branch_api.get_member_profile(id_member=int(member_id))
                    if result:
                        return result

            # If not found, try branch clients
            for branch_id in self.get_available_branch_ids():
                branch_api = MembersApi(api_client=self.get_branch_api(branch_id))
                if branch_api:
                    try:
                        result = branch_api.get_member_profile(id_member=int(member_id))
                        if result:
                            return result
                    except Exception as e:
                        logger.warning(
                            f"Failed to fetch member {member_id} from branch {branch_id}: {e}"
                        )

            return None

        except Exception as e:
            logger.error(f"Error fetching member {member_id}: {str(e)}")
            raise ValueError(f"Error fetching member {member_id}: {str(e)}")

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
        show_activity_data: bool = False,
    ) -> List[MembersApiViewModel]:
        """Fetch members with various filters.

        Args:
            name: Filter by member name
            email: Filter by email
            document: Filter by document number
            phone: Filter by phone number
            conversion_date_start: Filter by conversion start date
            conversion_date_end: Filter by conversion end date
            register_date_start: Filter by registration start date
            register_date_end: Filter by registration end date
            membership_start_date_start: Filter by membership start date
            membership_start_date_end: Filter by membership end date
            membership_cancel_date_start: Filter by cancellation start date
            membership_cancel_date_end: Filter by cancellation end date
            status: Filter by member status
            token_gympass: Filter by Gympass token
            ids_members: Comma-separated list of member IDs
            only_personal: Filter for personal training members only
            personal_type: Filter by personal training type
            show_activity_data: Include activity data in response

        Returns:
            List[MembersApiViewModel]: List of members matching the filters
        """
        try:
            members = []
            for branch_id in self.get_available_branch_ids():
                branch_api = MembersApi(api_client=self.get_branch_api(branch_id))
                if branch_api:
                    members.extend(
                        paginated_api_call(
                            api_func=branch_api.get_members,
                            unit_id=str(branch_id),
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
                    )

            return members

        except Exception as e:
            logger.error(f"Error fetching members: {str(e)}")
            raise ValueError(f"Error fetching members: {str(e)}")
