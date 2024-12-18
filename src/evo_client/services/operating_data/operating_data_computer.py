from typing import List, Dict, Any, Optional
from decimal import Decimal
from datetime import datetime

from ...models.gym_model import MembershipContract
from ...models.gym_model import Receivable
from ...models.gym_model import GymEntry
from ...models.gym_model import GymOperatingData, ReceivableStatus


class OperatingDataComputer:
    def compute_metrics(
        self,
        active_members: List[Dict],
        active_contracts: List[MembershipContract],
        prospects: List[Any],
        non_renewed: List[Any],
        receivables: List[Receivable],
        entries: List[GymEntry],
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
    ) -> GymOperatingData:
        """
        Compute operating metrics from raw data.

        Args:
            active_members: List of active member data
            active_contracts: List of active contracts
            prospects: List of prospects
            non_renewed: List of non-renewed members
            receivables: List of receivables
            entries: List of entries
            from_date: Start date for metrics calculation
            to_date: End date for metrics calculation

        Returns:
            GymOperatingData with computed metrics
        """
        # Calculate MRR from active contracts
        total_mrr = Decimal("0.00")

        for contract in active_contracts:
            if (
                hasattr(contract, "total_value")
                and contract.total_value
                and hasattr(contract, "plan")
                and contract.plan
                and hasattr(contract.plan, "minimum_commitment_months")
                and contract.plan.minimum_commitment_months
            ):
                # Convert contract value to monthly value
                monthly_value = Decimal(str(contract.total_value)) / Decimal(
                    str(contract.plan.minimum_commitment_months)
                )
                total_mrr += monthly_value

        # Calculate receivables metrics
        total_paid = Decimal("0.00")
        total_pending = Decimal("0.00")
        total_overdue = Decimal("0.00")

        for receivable in receivables:
            if receivable.status == ReceivableStatus.PAID:
                total_paid += receivable.amount or Decimal("0.00")
            elif receivable.status == ReceivableStatus.PENDING:
                total_pending += receivable.amount or Decimal("0.00")
            elif receivable.status == ReceivableStatus.OVERDUE:
                total_overdue += receivable.amount or Decimal("0.00")

        # Calculate member metrics
        total_active = len(active_members)
        total_churned = len(non_renewed)
        total_prospects = len(prospects)

        # Calculate churn rate
        churn_rate = Decimal("0.00")
        if total_active > 0:
            churned = Decimal(str(total_churned))
            active = Decimal(str(total_active))
            churn_rate = (churned / active) * Decimal("100")

        # Calculate cross-branch metrics
        member_home_branches = {}
        cross_branch_entries = []

        # Get home branches from contracts
        for contract in active_contracts:
            if hasattr(contract, "member_id") and hasattr(contract, "branch_id"):
                member_home_branches[contract.member_id] = contract.branch_id

        # Identify cross-branch entries
        for entry in entries:
            if (
                entry.member_id
                and entry.branch_id
                and entry.member_id in member_home_branches
                and entry.branch_id != member_home_branches[entry.member_id]
            ):
                cross_branch_entries.append(entry)

        # Calculate multi-unit percentage
        multi_unit_members = sum(
            1
            for c in active_contracts
            if hasattr(c, "plan") and getattr(c.plan, "access_branches", False)
        )

        multi_unit_percentage = Decimal("0.00")
        if total_active > 0:
            multi = Decimal(str(multi_unit_members))
            total = Decimal(str(total_active))
            multi_unit_percentage = (multi / total) * Decimal("100")

        return GymOperatingData(
            active_members=active_members,
            active_contracts=active_contracts,
            prospects=prospects,
            non_renewed_members=non_renewed,
            receivables=receivables,
            recent_entries=entries,
            data_from=from_date,
            data_to=to_date,
            total_active_members=total_active,
            total_churned_members=total_churned,
            total_prospects=total_prospects,
            mrr=total_mrr,
            churn_rate=churn_rate,
            total_paid=total_paid,
            total_pending=total_pending,
            total_overdue=total_overdue,
            cross_branch_entries=cross_branch_entries,
            multi_unit_member_percentage=multi_unit_percentage,
        )
