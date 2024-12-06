from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List

from evo_client.api.gym_api import GymApi
from evo_client.models.gym_model import (
    GymKnowledgeBase, GymOperatingData, MembersFiles,
    GymPlan, MembershipStatus, MemberProfile
)

def print_branch_summary(branch_id: str, knowledge_base: GymKnowledgeBase):
    """Print summary of branch information."""
    print(f"\n=== Branch {branch_id} Summary ===")
    print(f"Name: {knowledge_base.name}")
    print(f"Location: {knowledge_base.addresses[0].city}, {knowledge_base.addresses[0].state}")
    
    # Show multi-unit plans
    multi_unit_plans = [p for p in knowledge_base.plans if p.multi_unit_access]
    print(f"\nMulti-Unit Plans ({len(multi_unit_plans)}):")
    for plan in multi_unit_plans:
        print(f"- {plan.name}: ${plan.price}/month")
        print(f"  Allowed branches: {plan.allowed_branch_ids}")
        if plan.max_branch_visits_per_month:
            print(f"  Max visits/month: {plan.max_branch_visits_per_month}")

def print_operating_metrics(branch_id: str, data: GymOperatingData):
    """Print key operating metrics for a branch."""
    print(f"\n=== Branch {branch_id} Metrics ===")
    print(f"Active Members: {data.total_active_members}")
    print(f"Multi-Unit Members: {data.multi_unit_member_percentage}%")
    print(f"Cross-Branch Revenue: ${data.cross_branch_revenue}")
    print(f"Cross-Branch Visits: {len(data.cross_branch_entries)}")

def analyze_member_activity(members_files: MembersFiles):
    """Analyze and print member activity across branches."""
    print("\n=== Member Activity Analysis ===")
    
    for member_id, profile in members_files.members.items():
        if not isinstance(profile, MemberProfile):
            continue
            
        print(f"\nMember {member_id}:")
        if profile.current_contract and profile.current_contract.plan.multi_unit_access:
            print("- Has multi-unit access")
            
            # Group entries by branch
            branch_visits: Dict[int, int] = {}
            for entry in profile.entries_history:
                if entry.branch_id:
                    branch_visits[entry.branch_id] = branch_visits.get(entry.branch_id, 0) + 1
            
            print("Branch visit distribution:")
            for branch_id, visits in branch_visits.items():
                print(f"  Branch {branch_id}: {visits} visits")

def main():
    # Initialize GymApi with multiple branches
    gym_api = GymApi(branch_credentials=[
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
    ])

    # Set date range for analysis
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    # Get knowledge base for all branches
    knowledge_bases = gym_api.get_gym_knowledge_base()
    if isinstance(knowledge_bases, List):
        for kb, branch_id in zip(knowledge_bases, ["1", "2", "3"]):
            print_branch_summary(branch_id, kb)

    # Get operating data for all branches
    operating_data = gym_api.get_operating_data(
        from_date=start_date,
        to_date=end_date
    )
    if isinstance(operating_data, List):
        for data, branch_id in zip(operating_data, ["1", "2", "3"]):
            print_operating_metrics(branch_id, data)

    # Analyze specific members across all branches
    member_ids = [1, 2, 3]  # Example member IDs
    members_data = gym_api.get_members_files(
        member_ids=member_ids,
        from_date=start_date,
        to_date=end_date
    )
    if isinstance(members_data, List):
        for data in members_data:
            if isinstance(data, MembersFiles):
                analyze_member_activity(data)
    elif isinstance(members_data, MembersFiles):
        analyze_member_activity(members_data)

    # Example: Get data for specific branches only
    print("\n=== Specific Branch Analysis ===")
    branch_subset = ["1", "2"]
    subset_data = gym_api.get_operating_data(
        branch_ids=branch_subset,
        from_date=start_date,
        to_date=end_date
    )
    if isinstance(subset_data, List):
        for data, branch_id in zip(subset_data, branch_subset):
            print_operating_metrics(branch_id, data)

if __name__ == "__main__":
    main() 