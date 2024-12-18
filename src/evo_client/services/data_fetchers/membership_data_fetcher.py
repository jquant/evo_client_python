from typing import List, Optional, Dict
from evo_client.api.membership_api import MembershipApi
from evo_client.core.api_client import ApiClient
from evo_client.models.contratos_resumo_api_view_model import ContratosResumoApiViewModel
from evo_client.utils.pagination_utils import paginated_api_call
from evo_client.models.w12_utils_category_membership_view_model import W12UtilsCategoryMembershipViewModel
from . import BaseDataFetcher

class MembershipDataFetcher(BaseDataFetcher):
    """Handles fetching and processing membership-related data."""
    
    def __init__(self, membership_api: MembershipApi, branch_api_clients: Optional[Dict[str, ApiClient]] = None):
        super().__init__(membership_api, branch_api_clients)

    def fetch_memberships(
        self,
        membership_id: Optional[int] = None,
        name: Optional[str] = None,
        active: Optional[bool] = None,
    ) -> List[ContratosResumoApiViewModel]:
        """Fetch membership plans with optional filtering."""
        result = paginated_api_call(
            api_func=self.api.get_memberships,
            parallel_units=self.branch_ids,
            membership_id=membership_id,
            name=name,
            active=active,
            pagination_type="skip_take"
        )
        
        return result
    
    def fetch_membership_categories(self) -> List[W12UtilsCategoryMembershipViewModel]:
        """Fetch membership categories."""
        result = self.api.get_categories()
        return result
