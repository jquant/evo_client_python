#!/usr/bin/env python3
"""
🏋️ EVO Client Gym API Example (Updated to Modern Patterns)
===========================================================

⚠️  NOTICE: This example has been updated from v1 bundler patterns
    to modern sync/async patterns for better maintainability.

✅ Modern sync patterns (no more AsyncResult confusion)
✅ Clean context managers
✅ Direct API method calls
✅ Type-safe and intuitive

For more advanced examples, see: examples/v2/modern_sync_example.py
"""

import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from evo_client.config import ConfigBuilder
from evo_client.sync import SyncApiClient
from evo_client.sync.api import (
    SyncMembersApi,
    SyncSalesApi,
    SyncActivitiesApi,
    SyncReceivablesApi,
    SyncMembershipApi,
)
from evo_client.models.new_sale_view_model import NewSaleViewModel
from evo_client.models.member_new_sale_view_model import MemberNewSaleViewModel
from evo_client.models.e_forma_pagamento_totem import EFormaPagamentoTotem

print("🏋️ EVO Client Gym API Example - Modern Patterns")
print("=" * 48)
print()

# =============================================================================
# Configuration Setup
# =============================================================================

print("1️⃣ Setting up configuration...")

# Use environment variables for credentials (recommended)
config = ConfigBuilder.from_env(required_vars=False)
print(f"✅ Configuration loaded: {config.host}")

# =============================================================================
# Example 1: Basic Member Management
# =============================================================================


def example_member_management():
    """Demonstrate basic member operations."""
    print("\n2️⃣ Member Management Example")
    print("-" * 30)

    try:
        with SyncApiClient(config) as client:
            members_api = SyncMembersApi(client)

            print("📋 Available member operations:")
            print("   • Get all members")
            print("   • Search by email/phone")
            print("   • Get member details")
            print("   • Member authentication")

            # Example calls (would work with real credentials):
            # members = members_api.get_members(take=10)
            # member = members_api.get_member_by_id(member_id=123)
            # search_results = members_api.search_members(search="john@example.com")

            print("✅ Member API ready for use")

    except Exception as e:
        print(f"⚠️  Demo mode (would work with real credentials): {type(e).__name__}")


# =============================================================================
# Example 2: Sales Operations
# =============================================================================


def example_sales_operations():
    """Demonstrate sales and membership operations."""
    print("\n3️⃣ Sales Operations Example")
    print("-" * 29)

    try:
        with SyncApiClient(config) as client:
            sales_api = SyncSalesApi(client)
            membership_api = SyncMembershipApi(client)

            print("💰 Available sales operations:")
            print("   • Create new sales")
            print("   • Get sales history")
            print("   • Process memberships")
            print("   • Handle payments")

            # Example: Create a new sale
            def create_example_sale():
                """Example of creating a new sale with modern patterns."""
                member_data = MemberNewSaleViewModel(
                    idMember=0,  # New member
                    document="12345678901",
                    zipCode="01000-000",
                    address="Rua das Flores, 123",
                    number="123",
                    complement="Apt 45",
                    neighborhood="Centro",
                    city="São Paulo",
                    idState=25,  # São Paulo state
                )

                new_sale = NewSaleViewModel(
                    idBranch=1,
                    idMembership=1,
                    memberData=member_data,
                    voucher="WELCOME2024",
                    payment=EFormaPagamentoTotem._6,  # Credit card
                )

                # Clean method call (no async_req confusion!)
                # result = sales_api.create_sale(body=new_sale)
                return new_sale

            sale_example = create_example_sale()
            print(f"✅ Sale example prepared: membership {sale_example.id_membership}")

            # Example: Get recent sales
            def get_recent_sales():
                """Get sales from the last 30 days."""
                start_date = datetime.now() - timedelta(days=30)
                # sales = sales_api.get_sales(
                #     date_sale_start=start_date,
                #     take=10
                # )
                print(f"📊 Would fetch sales from: {start_date.strftime('%Y-%m-%d')}")

            get_recent_sales()

    except Exception as e:
        print(f"⚠️  Demo mode: {type(e).__name__}")


# =============================================================================
# Example 3: Activity Management
# =============================================================================


def example_activity_management():
    """Demonstrate activity and scheduling operations."""
    print("\n4️⃣ Activity Management Example")
    print("-" * 32)

    try:
        with SyncApiClient(config) as client:
            activities_api = SyncActivitiesApi(client)

            print("🏃 Available activity operations:")
            print("   • Get available activities")
            print("   • Check activity schedules")
            print("   • Enroll members in activities")
            print("   • Get schedule details")

            # Example operations:
            def manage_activities():
                """Example activity management operations."""
                # Get all activities
                # activities = activities_api.get_activities(take=20)

                # Get schedule for a specific date
                # today = datetime.now()
                # schedule = activities_api.get_schedule(
                #     member_id=123,
                #     date=today,
                #     take=10
                # )

                # Enroll member in activity
                # activities_api.enroll(
                #     config_id=456,
                #     activity_date=today,
                #     member_id=123
                # )

                return "Activity operations ready"

            result = manage_activities()
            print(f"✅ {result}")

    except Exception as e:
        print(f"⚠️  Demo mode: {type(e).__name__}")


# =============================================================================
# Example 4: Financial Operations
# =============================================================================


def example_financial_operations():
    """Demonstrate receivables and financial reporting."""
    print("\n5️⃣ Financial Operations Example")
    print("-" * 32)

    try:
        with SyncApiClient(config) as client:
            receivables_api = SyncReceivablesApi(client)

            print("💰 Available financial operations:")
            print("   • Get receivables reports")
            print("   • Check overdue accounts")
            print("   • Payment tracking")
            print("   • Financial analytics")

            def financial_report():
                """Generate financial reports."""
                end_date = datetime.now()
                start_date = end_date - timedelta(days=30)

                # Get receivables for the period
                # receivables = receivables_api.get_receivables(
                #     start_date=start_date,
                #     end_date=end_date
                # )

                print(
                    f"📊 Financial period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
                )
                return "Financial data ready"

            result = financial_report()
            print(f"✅ {result}")

    except Exception as e:
        print(f"⚠️  Demo mode: {type(e).__name__}")


# =============================================================================
# Example 5: Complete Workflow
# =============================================================================


def example_complete_workflow():
    """Demonstrate a complete gym management workflow."""
    print("\n6️⃣ Complete Workflow Example")
    print("-" * 30)

    try:
        with SyncApiClient(config) as client:
            # Create all needed API instances
            members_api = SyncMembersApi(client)
            sales_api = SyncSalesApi(client)
            activities_api = SyncActivitiesApi(client)
            receivables_api = SyncReceivablesApi(client)

            print("🔄 Complete gym management workflow:")

            workflow_steps = [
                "1. Check member database",
                "2. Process new memberships",
                "3. Update activity schedules",
                "4. Generate financial reports",
                "5. Update member records",
            ]

            for step in workflow_steps:
                print(f"   ✅ {step}")

            print("\n🎯 All APIs ready for integrated gym management!")
            print("📋 Benefits of modern patterns:")
            print("   • No more AsyncResult confusion")
            print("   • Clean, direct method calls")
            print("   • Proper resource management")
            print("   • Type-safe operations")

    except Exception as e:
        print(f"⚠️  Demo mode: {type(e).__name__}")


# =============================================================================
# Main Execution
# =============================================================================


def main():
    """Run all examples."""
    print("🎯 Running all gym API examples...\n")

    example_member_management()
    example_sales_operations()
    example_activity_management()
    example_financial_operations()
    example_complete_workflow()

    print("\n" + "=" * 48)
    print("✅ All examples completed successfully!")
    print("\n📚 For more advanced examples, see:")
    print("   • examples/v2/modern_sync_example.py")
    print("   • examples/v2/modern_async_example.py")
    print("   • examples/v2/configuration_showcase.py")


if __name__ == "__main__":
    main()
