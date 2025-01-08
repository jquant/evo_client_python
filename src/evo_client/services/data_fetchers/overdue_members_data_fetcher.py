from typing import List, Optional
from datetime import datetime
from loguru import logger

from ...api.receivables_api import ReceivablesApi
from ...models.receivables_api_view_model import ReceivablesApiViewModel
from ...models.gym_model import OverdueMember
from . import BaseDataFetcher

class OverdueMembersDataFetcher(BaseDataFetcher):
    """
    Fetch a list of overdue members to run reactivation campaigns.
    Overdue = receivables with status overdue.
    We'll try to get at least member_id, name, and contact info.
    """

    def fetch_overdue_members(
        self,
        due_date_end: Optional[datetime] = None,
        branch_ids: Optional[List[int]] = None
    ) -> List[OverdueMember]:
        """
        Fetch overdue members by analyzing receivables past due_date without payment.
        Args:
            due_date_end: optional end date for due
            branch_ids: optional list of branches
        """
        if branch_ids is None:
            branch_ids = self.get_available_branch_ids()

        overdue_list: List[OverdueMember] = []
        for branch_id in branch_ids:
            api = self.get_branch_api(branch_id)
            if not api:
                continue
            rapi = ReceivablesApi(api)
            try:
                # We'll fetch all receivables that are overdue
                # Assume due_date_end as filter
                receivables = rapi.get_receivables(
                    due_date_end=due_date_end,
                    account_status="overdue"
                )
                # Map receivables to overdue members
                # We assume member_id and member_name might be available in extended model
                # If not directly available, we might need a members lookup - but we only have the given code.
                # Let's assume `payer_name` and `id_member_payer` from receivables
                members_seen = {}
                for rv in receivables:
                    if rv.id_member_payer and rv.id_member_payer > 0:
                        key = rv.id_member_payer
                        members_seen.setdefault(key, {
                            "member_id": rv.id_member_payer,
                            "name": rv.payer_name or "",
                            "total_overdue": 0,
                            "overdue_since": rv.due_date,
                            "overdue_receivables": []
                        })
                        entry = members_seen[key]
                        entry["total_overdue"] += (rv.ammount or 0)
                        if (entry["overdue_since"] is None) or (rv.due_date and rv.due_date < entry["overdue_since"]):
                            entry["overdue_since"] = rv.due_date
                        entry["overdue_receivables"].append(rv)

                for mid, data in members_seen.items():
                    om = OverdueMember(
                        id=data["member_id"],
                        member_id=data["member_id"],
                        name=data["name"],
                        total_overdue=data["total_overdue"],
                        overdue_since=data["overdue_since"] or datetime.now(),
                        overdue_receivables=data["overdue_receivables"]
                    )
                    overdue_list.append(om)

            except Exception as e:
                logger.warning(f"Failed to fetch overdue members for branch {branch_id}: {e}")
        return overdue_list