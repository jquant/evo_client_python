from typing import List, Optional, Dict
from ...api.membership_api import MembershipApi
from ...core.api_client import ApiClient
from ...models.contratos_resumo_api_view_model import (
    ContratosResumoApiViewModel,
)
from ...utils.pagination_utils import paginated_api_call
from ...models.w12_utils_category_membership_view_model import (
    W12UtilsCategoryMembershipViewModel,
)
from . import BaseDataFetcher
from loguru import logger


class MembershipDataFetcher(BaseDataFetcher[MembershipApi]):
    """Handles fetching and processing membership-related data."""

    def __init__(
        self,
        membership_api: MembershipApi,
        branch_api_clients: Optional[Dict[str, ApiClient]] = None,
    ):
        """Initialize the membership data fetcher.

        Args:
            membership_api: The membership API instance
            branch_api_clients: Optional dictionary mapping branch IDs to their API clients
        """
        super().__init__(membership_api, branch_api_clients)

    def fetch_memberships(
        self,
        membership_id: Optional[int] = None,
        name: Optional[str] = None,
        active: Optional[bool] = None,
        default_client: bool = True,
    ) -> List[ContratosResumoApiViewModel]:
        """Fetch membership plans with optional filtering.

        Args:
            membership_id: Filter by membership ID
            name: Filter by membership name
            active: Filter by active status

        Returns:
            List[ContratosResumoApiViewModel]: List of membership plans matching the filters
        """
        try:
            # Get memberships from default client
            if default_client:
                memberships = paginated_api_call(
                    api_func=self.api.get_memberships,
                    unit_id="default",
                    membership_id=membership_id,
                    name=name,
                    active=active,
                    pagination_type="skip_take",
                )
            else:
                memberships = []
                for branch_id in self.get_available_branch_ids():
                    branch_api = self.get_branch_api(branch_id, MembershipApi)
                    if branch_api:
                        result = paginated_api_call(
                            api_func=branch_api.get_memberships,
                            unit_id=str(branch_id),
                            membership_id=membership_id,
                            name=name,
                            active=active,
                            pagination_type="skip_take",
                        )
                        if result:
                            memberships.extend(result)

            return memberships

        except Exception as e:
            logger.error(f"Error fetching memberships: {str(e)}")
            raise ValueError(f"Error fetching memberships: {str(e)}")

    def fetch_membership_categories(self) -> List[W12UtilsCategoryMembershipViewModel]:
        """Fetch membership categories.

        Returns:
            List[W12UtilsCategoryMembershipViewModel]: List of membership categories
        """
        try:
            categories = []

            # Get categories from default client
            result = self.api.get_categories()
            if result:
                categories.extend(result)

            # Get categories from branch clients
            for branch_id in self.get_available_branch_ids():
                branch_api = self.get_branch_api(branch_id, MembershipApi)
                if branch_api:
                    try:
                        branch_result = branch_api.get_categories()
                        if branch_result:
                            categories.extend(branch_result)
                    except Exception as e:
                        logger.warning(
                            f"Failed to fetch categories for branch {branch_id}: {e}"
                        )

            # Remove duplicates (if any)
            seen_categories = set()
            unique_categories = []
            for category in categories:
                if category.id not in seen_categories:
                    seen_categories.add(category.id)
                    unique_categories.append(category)

            return unique_categories

        except Exception as e:
            logger.error(f"Error fetching membership categories: {str(e)}")
            raise ValueError(f"Error fetching membership categories: {str(e)}")
