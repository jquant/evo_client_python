#!/usr/bin/env python3
"""
🏢 EVO Client Multi-Unit Example (Updated to Modern Patterns)
============================================================

⚠️  NOTICE: This example has been updated from v1 bundler patterns
    to modern sync/async patterns for better maintainability.

✅ Modern multi-branch management
✅ Clean configuration patterns
✅ Direct API method calls
✅ Proper resource management

For more advanced examples, see: examples/v2/modern_sync_example.py
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List

from evo_client.config import ConfigBuilder
from evo_client.sync import SyncApiClient
from evo_client.sync.api import (
    SyncMembersApi,
    SyncSalesApi,
    SyncConfigurationApi,
    SyncReceivablesApi,
    SyncEntriesApi,
)

print("🏢 EVO Client Multi-Unit Example - Modern Patterns")
print("=" * 51)
print()

# =============================================================================
# Multi-Branch Configuration Setup
# =============================================================================


def setup_multi_branch_configs() -> List[Dict[str, str]]:
    """Set up configurations for multiple branches."""
    print("🔧 Setting up multi-branch configurations...")

    # Example branch configurations (replace with real credentials)
    branch_configs = [
        {
            "branch_id": "1",
            "name": "Downtown Branch",
            "username": os.getenv("EVO_BRANCH1_USERNAME", "branch1_dns"),
            "password": os.getenv("EVO_BRANCH1_PASSWORD", "branch1_secret"),
        },
        {
            "branch_id": "2",
            "name": "Mall Branch",
            "username": os.getenv("EVO_BRANCH2_USERNAME", "branch2_dns"),
            "password": os.getenv("EVO_BRANCH2_PASSWORD", "branch2_secret"),
        },
        {
            "branch_id": "3",
            "name": "Suburb Branch",
            "username": os.getenv("EVO_BRANCH3_USERNAME", "branch3_dns"),
            "password": os.getenv("EVO_BRANCH3_PASSWORD", "branch3_secret"),
        },
    ]

    print(f"✅ Configured {len(branch_configs)} branches")
    for branch in branch_configs:
        print(f"   • {branch['name']} (ID: {branch['branch_id']})")

    return branch_configs


# =============================================================================
# Branch Analysis Functions
# =============================================================================


def analyze_branch_configuration(branch_config: Dict[str, str], host: str) -> Dict:
    """Analyze configuration for a single branch."""
    print(f"\n📊 Analyzing {branch_config['name']}...")

    try:
        # Create configuration for this branch
        config = ConfigBuilder.basic_auth(
            host=host,
            username=branch_config["username"],
            password=branch_config["password"],
        )

        with SyncApiClient(config) as client:
            config_api = SyncConfigurationApi(client)
            members_api = SyncMembersApi(client)

            # Get branch configuration
            branch_configs = config_api.get_branch_config()
            card_flags = config_api.get_card_flags()

            # Get sample member data
            try:
                sample_members = members_api.get_members(take=5)
                member_count = len(sample_members) if sample_members else 0
            except Exception:
                member_count = 0

            analysis = {
                "branch_id": branch_config["branch_id"],
                "name": branch_config["name"],
                "config_items": len(branch_configs) if branch_configs else 0,
                "payment_methods": len(card_flags) if card_flags else 0,
                "sample_member_count": member_count,
                "status": "accessible",
            }

            print(
                f"   ✅ {analysis['name']}: {analysis['config_items']} configs, {analysis['payment_methods']} payment methods"
            )
            return analysis

    except Exception as e:
        print(f"   ❌ {branch_config['name']}: {type(e).__name__}")
        return {
            "branch_id": branch_config["branch_id"],
            "name": branch_config["name"],
            "status": "error",
            "error": str(e),
        }


def analyze_sales_performance(branch_config: Dict[str, str], days: int = 30) -> Dict:
    """Analyze sales performance for a branch."""
    print(f"\n💰 Sales analysis for {branch_config['name']}...")

    try:
        config = ConfigBuilder.basic_auth(
            host=branch_config["host"],
            username=branch_config["username"],
            password=branch_config["password"],
        )

        with SyncApiClient(config) as client:
            sales_api = SyncSalesApi(client)
            receivables_api = SyncReceivablesApi(client)

            # Get recent sales data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            try:
                # Get sales for the period
                sales_data = sales_api.get_sales(
                    date_sale_start=start_date, date_sale_end=end_date, take=100
                )
                sales_count = len(sales_data) if sales_data else 0
            except Exception:
                sales_count = 0

            try:
                # Get receivables data
                receivables_data = receivables_api.get_receivables()
                receivables_count = len(receivables_data) if receivables_data else 0
            except Exception:
                receivables_count = 0

            performance = {
                "branch_id": branch_config["branch_id"],
                "name": branch_config["name"],
                "period_days": days,
                "sales_count": sales_count,
                "receivables_count": receivables_count,
                "status": "analyzed",
            }

            print(
                f"   📈 {sales_count} sales, {receivables_count} receivables in {days} days"
            )
            return performance

    except Exception as e:
        print(f"   ❌ Analysis failed: {type(e).__name__}")
        return {
            "branch_id": branch_config["branch_id"],
            "name": branch_config["name"],
            "status": "error",
            "error": str(e),
        }


def analyze_member_activity(branch_config: Dict[str, str]) -> Dict:
    """Analyze member activity for a branch."""
    print(f"\n👥 Member activity for {branch_config['name']}...")

    try:
        config = ConfigBuilder.basic_auth(
            host=branch_config["host"],
            username=branch_config["username"],
            password=branch_config["password"],
        )

        with SyncApiClient(config) as client:
            members_api = SyncMembersApi(client)
            entries_api = SyncEntriesApi(client)

            # Get member statistics
            try:
                members = members_api.get_members(take=20)
                member_count = len(members) if members else 0
            except Exception:
                member_count = 0

            try:
                # Get recent entries
                today = datetime.now()
                entries = entries_api.get_entries(
                    register_date_start=today - timedelta(days=7),
                    register_date_end=today,
                )
                entry_count = len(entries) if entries else 0
            except Exception:
                entry_count = 0

            activity = {
                "branch_id": branch_config["branch_id"],
                "name": branch_config["name"],
                "member_sample": member_count,
                "weekly_entries": entry_count,
                "avg_daily_entries": entry_count / 7 if entry_count > 0 else 0,
                "status": "analyzed",
            }

            print(f"   🏃 {member_count} members, {entry_count} entries this week")
            return activity

    except Exception as e:
        print(f"   ❌ Analysis failed: {type(e).__name__}")
        return {
            "branch_id": branch_config["branch_id"],
            "name": branch_config["name"],
            "status": "error",
            "error": str(e),
        }


# =============================================================================
# Multi-Unit Analysis
# =============================================================================


def generate_multi_unit_report(branch_configs: List[Dict[str, str]], host: str) -> Dict:
    """Generate comprehensive multi-unit analysis report."""
    print("\n📊 Generating multi-unit analysis report...")

    report = {
        "timestamp": datetime.now().isoformat(),
        "total_branches": len(branch_configs),
        "branch_analyses": [],
        "sales_performance": [],
        "member_activity": [],
        "summary": {},
    }

    # Analyze each branch
    accessible_branches = 0
    total_sales = 0
    total_members = 0

    for branch_config in branch_configs:
        # Configuration analysis
        config_analysis = analyze_branch_configuration(branch_config, host)
        report["branch_analyses"].append(config_analysis)

        if config_analysis["status"] == "accessible":
            accessible_branches += 1

            # Sales analysis
            sales_analysis = analyze_sales_performance(branch_config)
            report["sales_performance"].append(sales_analysis)
            total_sales += sales_analysis.get("sales_count", 0)

            # Member activity analysis
            activity_analysis = analyze_member_activity(branch_config)
            report["member_activity"].append(activity_analysis)
            total_members += activity_analysis.get("member_sample", 0)

    # Generate summary
    report["summary"] = {
        "accessible_branches": accessible_branches,
        "total_branches": len(branch_configs),
        "accessibility_rate": f"{(accessible_branches/len(branch_configs)*100):.1f}%",
        "total_sales_sample": total_sales,
        "total_member_sample": total_members,
        "avg_sales_per_branch": (
            total_sales / accessible_branches if accessible_branches > 0 else 0
        ),
        "avg_members_per_branch": (
            total_members / accessible_branches if accessible_branches > 0 else 0
        ),
    }

    return report


def print_summary_report(report: Dict):
    """Print a formatted summary of the multi-unit analysis."""
    print("\n" + "=" * 51)
    print("🎯 MULTI-UNIT ANALYSIS SUMMARY")
    print("=" * 51)

    summary = report["summary"]
    print(
        f"📊 Branches Analyzed: {summary['accessible_branches']}/{summary['total_branches']} ({summary['accessibility_rate']})"
    )
    print(f"💰 Total Sales Sample: {summary['total_sales_sample']}")
    print(f"👥 Total Member Sample: {summary['total_member_sample']}")
    print(f"📈 Avg Sales/Branch: {summary['avg_sales_per_branch']:.1f}")
    print(f"👤 Avg Members/Branch: {summary['avg_members_per_branch']:.1f}")

    print(f"\n📋 Branch Status:")
    for analysis in report["branch_analyses"]:
        status_icon = "✅" if analysis["status"] == "accessible" else "❌"
        print(f"   {status_icon} {analysis['name']} (ID: {analysis['branch_id']})")

    print(f"\n🎉 Multi-unit analysis completed!")
    print(f"📚 For more advanced examples, see:")
    print(f"   • examples/v2/modern_sync_example.py")
    print(f"   • examples/v2/modern_async_example.py")


# =============================================================================
# Main Execution
# =============================================================================


def main():
    """Run the multi-unit analysis."""
    print("🎯 Starting multi-unit gym analysis...\n")
    host = os.getenv("EVO_HOST", "https://evo-integracao-api.w12app.com.br")

    # Setup configurations
    branch_configs = setup_multi_branch_configs()

    # Generate comprehensive report
    report = generate_multi_unit_report(branch_configs, host)

    # Print summary
    print_summary_report(report)


if __name__ == "__main__":
    main()
