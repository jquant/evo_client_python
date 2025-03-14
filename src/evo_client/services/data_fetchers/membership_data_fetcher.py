from typing import List, Optional

from loguru import logger

from ...api.membership_api import MembershipApi
from ...models.contratos_resumo_api_view_model import ContratosResumoApiViewModel
from ...models.w12_utils_category_membership_view_model import (
    W12UtilsCategoryMembershipViewModel,
)
from ...utils.pagination_utils import paginated_api_call
from . import BaseDataFetcher


class MembershipDataFetcher(BaseDataFetcher):
    """Handles fetching and processing membership-related data."""

    def fetch_memberships(
        self,
        membership_id: Optional[int] = None,
        name: Optional[str] = None,
        active: Optional[bool] = None,
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
            memberships = []
            for branch_id in self.get_available_branch_ids():
                branch_api = MembershipApi(api_client=self.get_branch_api(branch_id))
                if branch_api:
                    result = paginated_api_call(
                        api_func=branch_api.get_memberships,
                        branch_id=str(branch_id),
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
            for branch_id in self.get_available_branch_ids():
                branch_api = MembershipApi(api_client=self.get_branch_api(branch_id))
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
