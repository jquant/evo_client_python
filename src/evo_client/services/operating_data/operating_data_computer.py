from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from ...models.contratos_resumo_api_view_model import ContratosResumoApiViewModel
from ...models.gym_model import GymEntry, GymOperatingData
from ...models.members_api_view_model import MembersApiViewModel
from ...models.prospects_resumo_api_view_model import ProspectsResumoApiViewModel
from ...models.receivables_api_view_model import ReceivablesApiViewModel


class OperatingDataComputer:
    def compute_metrics(
        self,
        active_members: List[MembersApiViewModel],
        prospects: List[ProspectsResumoApiViewModel],
        non_renewed: List[MembersApiViewModel],
        receivables: List[ReceivablesApiViewModel],
        entries: List[GymEntry],
        active_contracts: List[ContratosResumoApiViewModel],
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        previous_data: Optional[GymOperatingData] = None,
    ) -> GymOperatingData:
        """
        Compute operating metrics from raw data, including advanced metrics.

        Args:
            active_members: List of active members for the current period
            prospects: List of prospects for the current period
            non_renewed: List of non-renewed members in the current period
            receivables: List of receivables in the current period
            entries: List of gym entries in the current period
            active_contracts: List of active membership contracts in the current period
            from_date: Start date of the current period
            to_date: End date of the current period
            previous_data: GymOperatingData for the previous period (for GRR, NRR calculations)

        Returns:
            GymOperatingData with computed metrics
        """

        total_active = len(active_members)
        total_churned = len(non_renewed)
        total_prospects = len(prospects)

        # Compute MRR from active contracts. Assume each contract has a monthly price attribute (like price).
        # We sum all contract prices to get MRR.
        # If no price attribute is found, default to 0.
        total_mrr = Decimal("0.00")
        for c in active_contracts:
            # Assuming c has a price attribute representing the monthly fee
            price = (
                Decimal(str(c.value))
                if hasattr(c, "value") and c.value is not None
                else Decimal("0.00")
            )
            total_mrr += price

        # ARR = MRR * 12
        arr = total_mrr * Decimal("12")

        # Calculate churn rate.
        # If previous_data is available, we use previous_data.total_active_members to determine churn.
        if previous_data and previous_data.total_active_members > 0:
            churn_rate = (
                Decimal(str(total_churned))
                / Decimal(str(previous_data.total_active_members))
            ) * Decimal("100")
        else:
            # Without previous data, we estimate churn as non_renewed/active currently. This is less accurate.
            if total_active + total_churned > 0:
                churn_rate = (
                    Decimal(str(total_churned))
                    / Decimal(str(total_active + total_churned))
                ) * Decimal("100")
            else:
                churn_rate = Decimal("0.00")

        # Receivables metrics
        total_paid = Decimal("0.00")
        total_pending = Decimal("0.00")
        total_overdue = Decimal("0.00")

        now = datetime.now()
        for r in receivables:
            amnt = Decimal(str(r.ammount or "0.00"))
            amnt_paid = Decimal(str(r.ammount_paid or "0.00"))
            if amnt_paid > 0:
                total_paid += amnt
            else:
                if r.due_date and r.due_date < now:
                    total_overdue += amnt
                else:
                    total_pending += amnt

        # ARPU = MRR / total_active_members if total_active > 0
        arpu = Decimal("0.00")
        if total_active > 0:
            arpu = total_mrr / Decimal(str(total_active))

        # LTV = ARPU / (churn_rate/100) if churn_rate > 0 else 0
        if churn_rate > 0:
            ltv = (arpu * Decimal("12")) / (churn_rate / Decimal("100"))
        else:
            ltv = Decimal("0.00")

        # Compute GRR and NRR if previous_data is available. Otherwise default to 100%.
        # We need to estimate MRR components:
        # new_mrr = MRR from members who joined this period and were not in previous
        # churned_mrr = MRR lost from members who left
        # expansion_mrr, contraction_mrr, reactivation_mrr are complex, we have no data for that detail.
        # We'll assume no expansions or contractions for simplicity:
        expansion_mrr = Decimal("0.00")
        contraction_mrr = Decimal("0.00")
        churned_mrr = Decimal("0.00")
        # If previous_data is available and had some MRR, estimate churned_mrr as (some fraction)
        if previous_data and previous_data.mrr > 0:
            # Let's estimate churned_mrr as MRR fraction proportional to churned members
            if previous_data.total_active_members > 0 and total_churned > 0:
                avg_prev_mrr_per_member = previous_data.mrr / Decimal(
                    str(previous_data.total_active_members)
                )
                churned_mrr = avg_prev_mrr_per_member * Decimal(str(total_churned))

        if previous_data and previous_data.mrr > 0:
            grr = ((previous_data.mrr - churned_mrr) / previous_data.mrr) * Decimal(
                "100"
            )
            nrr = (
                (previous_data.mrr + expansion_mrr - contraction_mrr - churned_mrr)
                / previous_data.mrr
            ) * Decimal("100")
        else:
            # No previous_data, default
            grr = Decimal("100.00")
            nrr = Decimal("100.00")

        # Multi-unit percentage and other metrics we can't compute from provided data:
        multi_unit_percentage = Decimal("0.00")

        # membership_growth_rate:
        # If previous_data provided,
        # growth = ((current_active - prev_active)/prev_active)*100
        membership_growth_rate = Decimal("0.00")
        if previous_data and previous_data.total_active_members > 0:
            membership_growth_rate = (
                (
                    Decimal(str(total_active))
                    - Decimal(str(previous_data.total_active_members))
                )
                / Decimal(str(previous_data.total_active_members))
            ) * Decimal("100")

        # class attendance rate:
        # We have entries and no direct info about classes. We'll just set it 0 for now.
        class_attendance_rate = Decimal("0.00")

        # average_visits_per_member:
        # If we have entries and active members,
        # average visits = total entries / total_active_members
        avg_visits_per_member = Decimal("0.00")
        if total_active > 0 and len(entries) > 0:
            avg_visits_per_member = Decimal(str(len(entries))) / Decimal(
                str(total_active)
            )

        data = GymOperatingData(
            active_members=[m.model_dump() for m in active_members],
            active_contracts=[c.model_dump() for c in active_contracts],
            prospects=[p.model_dump() for p in prospects],
            non_renewed_members=[nm.model_dump() for nm in non_renewed],
            receivables=[r.model_dump() for r in receivables],
            recent_entries=[e.model_dump() for e in entries],
            cross_branch_entries=[],
            data_from=from_date,
            data_to=to_date,
            mrr=total_mrr,
            arr=arr,
            average_revenue_per_member=arpu,
            lifetime_value=ltv,
            total_active_members=total_active,
            total_churned_members=total_churned,
            churn_rate=churn_rate,
            retention_rate=(
                Decimal("100") - churn_rate if total_active > 0 else Decimal("100")
            ),
            membership_growth_rate=membership_growth_rate,
            multi_unit_member_percentage=multi_unit_percentage,
            capacity_metrics=None,
            class_attendance_rate=class_attendance_rate,
            average_visits_per_member=avg_visits_per_member,
            total_prospects=total_prospects,
            total_paid=total_paid,
            total_pending=total_pending,
            total_overdue=total_overdue,
        )

        # Add GRR, NRR as attributes (not originally present)
        setattr(data, "grr", grr)
        setattr(data, "nrr", nrr)

        # Return computed data
        return data
