from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, NamedTuple
import asyncio

from evo_client.api.gym_api import GymApi
from evo_client.models.gym_model import (
    GymKnowledgeBase, GymOperatingData, GymEntry,
    GymPlan, MembershipStatus, MembershipContract
)

class RevenueMetrics(NamedTuple):
    """Revenue metrics for a specific period."""
    mrr: Decimal  # Monthly Recurring Revenue
    arr: Decimal  # Annual Recurring Revenue
    new_mrr: Decimal  # MRR from new members
    expansion_mrr: Decimal  # MRR from upgrades/add-ons
    contraction_mrr: Decimal  # MRR from downgrades
    churned_mrr: Decimal  # MRR lost from churned members
    reactivation_mrr: Decimal  # MRR from reactivated members
    net_mrr: Decimal  # Net MRR change
    grr: Decimal  # Gross Revenue Retention (%)
    nrr: Decimal  # Net Revenue Retention (%)

class ChainMetrics(NamedTuple):
    """Key business metrics for the gym chain."""
    acv: Decimal  # Average Contract Value
    arpu: Decimal  # Average Revenue Per User
    clv: Decimal  # Customer Lifetime Value
    churn_rate: Decimal  # Monthly churn rate (%)
    quick_ratio: Decimal  # (New + Expansion MRR) / (Contraction + Churned MRR)
    multi_unit_ratio: Decimal  # % of members with multi-unit access
    cross_branch_ratio: Decimal  # % of visits that are cross-branch

class ChainAnalytics:
    """Advanced analytics for the entire gym chain."""
    
    def __init__(self, operating_data_list: List[GymOperatingData], previous_month_data: Optional[List[GymOperatingData]] = None):
        self.current_data = operating_data_list
        self.previous_data = previous_month_data or []
        
        # Basic metrics
        self.total_active_members = sum(data.total_active_members for data in operating_data_list)
        self.total_revenue = sum(data.mrr for data in operating_data_list)
        self.total_cross_branch_revenue = sum(data.cross_branch_revenue for data in operating_data_list)
        
        # Aggregate all cross-branch entries
        self.cross_branch_entries: List[GymEntry] = []
        for data in operating_data_list:
            self.cross_branch_entries.extend(data.cross_branch_entries)
        
        # Calculate advanced metrics
        self.revenue_metrics = self._calculate_revenue_metrics()
        self.chain_metrics = self._calculate_chain_metrics()
        
        # Track branch performance
        self.branch_rankings = self._rank_branches(operating_data_list)
    
    def _calculate_revenue_metrics(self) -> RevenueMetrics:
        """Calculate detailed revenue metrics."""
        current_mrr = sum(data.mrr for data in self.current_data)
        previous_mrr = sum(data.mrr for data in self.previous_data) if self.previous_data else Decimal('0')
        
        # Calculate MRR components
        new_mrr = sum(
            contract.plan.price
            for data in self.current_data
            for contract in data.active_contracts
            if not any(c.member_id == contract.member_id for c in data.active_contracts)
        )
        
        churned_mrr = sum(
            contract.plan.price
            for data in self.previous_data
            for contract in data.active_contracts
            if not any(c.member_id == contract.member_id for c in self.current_data[0].active_contracts)
        ) if self.previous_data else Decimal('0')
        
        # Calculate expansion/contraction from plan changes
        expansion_mrr = Decimal('0')
        contraction_mrr = Decimal('0')
        if self.previous_data:
            for prev_data, curr_data in zip(self.previous_data, self.current_data):
                for curr_contract in curr_data.active_contracts:
                    prev_contract = next(
                        (c for c in prev_data.active_contracts if c.member_id == curr_contract.member_id),
                        None
                    )
                    if prev_contract:
                        diff = curr_contract.plan.price - prev_contract.plan.price
                        if diff > 0:
                            expansion_mrr += diff
                        elif diff < 0:
                            contraction_mrr += abs(diff)
        
        # Calculate reactivation MRR (from previously churned members)
        reactivation_mrr = Decimal('0')
        if self.previous_data:
            for data in self.current_data:
                for contract in data.active_contracts:
                    # Check if member was previously inactive or cancelled
                    was_churned = any(
                        not any(c.member_id == contract.member_id and c.status == MembershipStatus.ACTIVE 
                               for c in prev_data.active_contracts)
                        for prev_data in self.previous_data
                    )
                    if was_churned:
                        reactivation_mrr += contract.plan.price
        
        # Calculate net MRR change
        net_mrr = new_mrr + expansion_mrr + reactivation_mrr - contraction_mrr - churned_mrr
        
        # Calculate retention rates
        grr = (
            Decimal(str((previous_mrr - churned_mrr) / previous_mrr * 100))
            if previous_mrr > 0 else Decimal('100')
        )
        nrr = (
            Decimal(str((previous_mrr + expansion_mrr - contraction_mrr - churned_mrr) / previous_mrr * 100))
            if previous_mrr > 0 else Decimal('100')
        )
        
        return RevenueMetrics(
            mrr=Decimal(str(current_mrr)),
            arr=Decimal(str(current_mrr * 12)),
            new_mrr=Decimal(str(new_mrr)),
            expansion_mrr=expansion_mrr,
            contraction_mrr=contraction_mrr,
            churned_mrr=Decimal(str(churned_mrr)),
            reactivation_mrr=reactivation_mrr,
            net_mrr=net_mrr,
            grr=grr,
            nrr=nrr
        )
    
    def _calculate_chain_metrics(self) -> ChainMetrics:
        """Calculate chain-wide business metrics."""
        # Calculate Average Contract Value
        total_contract_value = sum(
            sum(contract.plan.price * Decimal(str(contract.plan.minimum_commitment_months)) 
                for contract in data.active_contracts)
            for data in self.current_data
        )
        total_contracts = sum(len(data.active_contracts) for data in self.current_data)
        acv = Decimal(str(total_contract_value / total_contracts)) if total_contracts > 0 else Decimal('0')
        
        # Calculate ARPU (Average Revenue Per User)
        arpu = Decimal(str(self.revenue_metrics.mrr / self.total_active_members)) if self.total_active_members > 0 else Decimal('0')
        
        # Calculate churn rate
        churned_members = sum(data.total_churned_members for data in self.current_data)
        churn_rate = (
            Decimal(str(churned_members)) / Decimal(str(self.total_active_members)) * Decimal('100')
            if self.total_active_members > 0 else Decimal('0')
        )
        
        # Estimate Customer Lifetime Value (CLV = ARPU / Churn Rate)
        clv = (
            Decimal(str(arpu * 12 / (churn_rate / Decimal('100'))))
            if churn_rate > 0 else Decimal('0')
        )
        
        # Calculate Quick Ratio (growth efficiency)
        denominator = self.revenue_metrics.contraction_mrr + self.revenue_metrics.churned_mrr
        quick_ratio = (
            Decimal(str((self.revenue_metrics.new_mrr + self.revenue_metrics.expansion_mrr) / denominator))
            if denominator > 0 else Decimal('999')
        )
        
        # Calculate multi-unit and cross-branch ratios
        total_multi_unit_members = sum(
            int(data.total_active_members * data.multi_unit_member_percentage / 100)
            for data in self.current_data
        )
        multi_unit_ratio = (
            Decimal(str(total_multi_unit_members)) / Decimal(str(self.total_active_members)) * Decimal('100')
            if self.total_active_members > 0 else Decimal('0')
        )
        
        total_visits = sum(len(data.recent_entries) for data in self.current_data)
        cross_branch_ratio = (
            Decimal(str(len(self.cross_branch_entries))) / Decimal(str(total_visits)) * Decimal('100')
            if total_visits > 0 else Decimal('0')
        )
        
        return ChainMetrics(
            acv=acv,
            arpu=arpu,
            clv=clv,
            churn_rate=churn_rate,
            quick_ratio=quick_ratio,
            multi_unit_ratio=multi_unit_ratio,
            cross_branch_ratio=cross_branch_ratio
        )
    
    def _rank_branches(self, operating_data_list: List[GymOperatingData]) -> Dict[str, List[int]]:
        """Rank branches by different metrics."""
        metrics = {
            'revenue': [(i, data.mrr) for i, data in enumerate(operating_data_list)],
            'members': [(i, data.total_active_members) for i, data in enumerate(operating_data_list)],
            'multi_unit': [(i, data.multi_unit_member_percentage) for i, data in enumerate(operating_data_list)],
            'retention': [(i, 100 - data.churn_rate) for i, data in enumerate(operating_data_list)]
        }
        
        rankings = {}
        for metric, values in metrics.items():
            sorted_branches = sorted(values, key=lambda x: x[1], reverse=True)
            rankings[metric] = [b[0] for b in sorted_branches]
            
        return rankings

def print_chain_summary(chain: ChainAnalytics, branch_ids: List[str]):
    """Print comprehensive chain-wide analytics."""
    print("\n=== Chain-Wide Revenue Metrics ===")
    print(f"MRR: ${chain.revenue_metrics.mrr:,.2f}")
    print(f"ARR: ${chain.revenue_metrics.arr:,.2f}")
    print(f"Net MRR Growth: ${chain.revenue_metrics.net_mrr:,.2f}")
    print(f"Gross Revenue Retention: {chain.revenue_metrics.grr:.1f}%")
    print(f"Net Revenue Retention: {chain.revenue_metrics.nrr:.1f}%")
    
    print("\n=== MRR Movement ===")
    print(f"New: ${chain.revenue_metrics.new_mrr:,.2f}")
    print(f"Expansion: ${chain.revenue_metrics.expansion_mrr:,.2f}")
    print(f"Contraction: ${chain.revenue_metrics.contraction_mrr:,.2f}")
    print(f"Churn: ${chain.revenue_metrics.churned_mrr:,.2f}")
    print(f"Reactivation: ${chain.revenue_metrics.reactivation_mrr:,.2f}")
    
    print("\n=== Chain-Wide Business Metrics ===")
    print(f"Average Contract Value: ${chain.chain_metrics.acv:,.2f}")
    print(f"Monthly ARPU: ${chain.chain_metrics.arpu:,.2f}")
    print(f"Customer Lifetime Value: ${chain.chain_metrics.clv:,.2f}")
    print(f"Monthly Churn Rate: {chain.chain_metrics.churn_rate:.1f}%")
    print(f"Quick Ratio: {chain.chain_metrics.quick_ratio:.2f}")
    print(f"Multi-Unit Membership Rate: {chain.chain_metrics.multi_unit_ratio:.1f}%")
    print(f"Cross-Branch Visit Rate: {chain.chain_metrics.cross_branch_ratio:.1f}%")
    
    print("\n=== Branch Rankings ===")
    for metric, ranks in chain.branch_rankings.items():
        print(f"\nTop branches by {metric}:")
        for i, branch_idx in enumerate(ranks[:3], 1):
            print(f"{i}. Branch {branch_ids[branch_idx]}")

async def main():
    # Initialize GymApi with multiple branches
    branch_credentials = [
        {
            "username": "branch1_user",
            "password": "branch1_pass",
            "branch_id": "1"
        },
        {
            "username": "branch2_user",
            "password": "branch2_pass",
            "branch_id": "2"
        },
        {
            "username": "branch3_user",
            "password": "branch3_pass",
            "branch_id": "3"
        }
    ]
    
    gym_api = GymApi(branch_credentials=branch_credentials)
    
    # Get current and previous month data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    prev_end_date = start_date
    prev_start_date = prev_end_date - timedelta(days=30)

    # Get operating data for current month
    current_data = await gym_api.get_operating_data(
        from_date=start_date,
        to_date=end_date
    )
    
    # Get operating data for previous month
    previous_data = await gym_api.get_operating_data(
        from_date=prev_start_date,
        to_date=prev_end_date
    )
    
    if isinstance(current_data, List) and isinstance(previous_data, List):
        branch_ids = ["1", "2", "3"]
        
        # Create chain analytics instance
        chain = ChainAnalytics(current_data, previous_data)
        
        # Print chain summary
        print_chain_summary(chain, branch_ids)

if __name__ == "__main__":
    asyncio.run(main()) 