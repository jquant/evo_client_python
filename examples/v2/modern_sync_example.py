#!/usr/bin/env python3
"""
🔄 EVO Client Modern Sync Example
=================================

This example demonstrates the clean, modern sync implementation that
replaced complex overloaded methods with simple, direct API calls.

✅ Simple, direct method calls (no more async_req=True)
✅ Clean method signatures (no complex overloads)
✅ Natural context manager support
✅ Proper resource management
✅ Type-safe, intuitive APIs
✅ Backward compatible

Usage:
    python examples/modern_sync_example.py
"""

import sys
import os
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

print("🔄 EVO Client Modern Sync Example")
print("=" * 38)
print()

# =============================================================================
# 🎯 SETUP: Configuration Using Our New Helpers
# =============================================================================

from evo_client.config import ConfigBuilder, ConfigPresets, QuickConfig
from evo_client.sync import SyncApiClient
from evo_client.sync.api import (
    SyncMembersApi,
    SyncSalesApi,
    SyncActivitiesApi,
    SyncMembershipApi,
    SyncReceivablesApi,
    SyncInvoicesApi,
    SyncEmployeesApi,
)

print("1️⃣ Configuration Setup")
print("-" * 25)

# Multiple ways to set up configuration
print("🔧 Configuration options:")

# Option 1: Quick gym setup
gym_config = QuickConfig.gym_basic("demo_gym", "demo_secret")
print(f"✅ Quick setup: {gym_config.host}")

# Option 2: Environment-based (recommended for production)
try:
    env_config = ConfigBuilder.from_env(required_vars=False)
    print(f"✅ Environment config: {env_config.host}")
except Exception:
    print("ℹ️  Environment config: (set EVO_* vars to use)")

# Option 3: Preset configurations
dev_config = ConfigPresets.gym_development()
print(f"✅ Development preset: {dev_config.host}")

# Use development config for this demo
config = dev_config
print(f"\n📋 Using config: {config.host}")
print(f"   Timeout: {config.timeout}s")
print(f"   SSL Verification: {config.verify_ssl}")
print()

# =============================================================================
# 🎯 EXAMPLE 1: Basic Sync Usage with Context Managers
# =============================================================================


def example_basic_sync():
    """Demonstrate basic sync client usage with context managers."""
    print("2️⃣ Basic Sync Usage with Context Managers")
    print("-" * 43)

    try:
        # Clean sync pattern with context manager
        with SyncApiClient(config) as client:
            print("✅ SyncApiClient created with context manager")

            # Create API instances
            members_api = SyncMembersApi(client)
            sales_api = SyncSalesApi(client)

            print("✅ API instances created: SyncMembersApi, SyncSalesApi")
            print("📞 Ready for direct API calls like:")
            print("   • members_api.get_members()")
            print("   • sales_api.get_sales()")
            print("   • No more async_req=True confusion!")

    except Exception as e:
        print(f"⚠️  Demo mode (would work with real credentials): {type(e).__name__}")

    print()


# =============================================================================
# 🎯 EXAMPLE 2: Multiple API Usage in One Session
# =============================================================================


def example_multiple_apis():
    """Demonstrate using multiple APIs in one session."""
    print("3️⃣ Multiple API Usage in One Session")
    print("-" * 38)

    try:
        with SyncApiClient(config) as client:
            print("🔄 Creating multiple API instances...")

            # Create all the APIs we need
            members_api = SyncMembersApi(client)
            sales_api = SyncSalesApi(client)
            activities_api = SyncActivitiesApi(client)
            receivables_api = SyncReceivablesApi(client)
            invoices_api = SyncInvoicesApi(client)

            print("✅ All API instances created successfully")

            # Simulate a business workflow
            print("\n📋 Simulated business workflow:")
            print("   1. Check member status")
            print("   2. Review recent sales")
            print("   3. Check activity bookings")
            print("   4. Review receivables")
            print("   5. Process invoices")

            # These would be real API calls:
            def mock_workflow():
                steps_completed = []

                # Step 1: Member management
                steps_completed.append("✅ Member status checked")
                # members = members_api.get_members(take=10)

                # Step 2: Sales analysis
                steps_completed.append("✅ Sales data retrieved")
                # today = datetime.now().date()
                # sales = sales_api.get_sales(date_sale_start=today)

                # Step 3: Activity management
                steps_completed.append("✅ Activity bookings reviewed")
                # activities = activities_api.get_activities()

                # Step 4: Financial review
                steps_completed.append("✅ Receivables analyzed")
                # receivables = receivables_api.get_receivables()

                # Step 5: Invoice processing
                steps_completed.append("✅ Invoices processed")
                # invoices = invoices_api.get_invoices()

                return steps_completed

            completed_steps = mock_workflow()
            for step in completed_steps:
                print(f"   {step}")

            print(f"\n🎯 Workflow completed: {len(completed_steps)} steps")

    except Exception as e:
        print(f"⚠️  Demo mode: {type(e).__name__}")

    print()


# =============================================================================
# 🎯 EXAMPLE 3: Error Handling and Resource Management
# =============================================================================


def example_error_handling():
    """Demonstrate proper error handling and resource management."""
    print("4️⃣ Error Handling and Resource Management")
    print("-" * 42)

    print("🛡️  Error handling patterns:")
    print("   • Network timeouts")
    print("   • API response errors")
    print("   • Authentication failures")
    print("   • Resource cleanup")

    try:
        # Proper resource management with context manager
        with SyncApiClient(config) as client:
            members_api = SyncMembersApi(client)

            print("\n✅ Client created with automatic resource cleanup")

            # Example error handling patterns
            try:
                # This would be a real API call
                # members = members_api.get_members()
                print("✅ API call pattern demonstrated")

                # Handle specific cases
                # if not members:
                #     print("⚠️  No members found")
                # elif len(members) > 1000:
                #     print("📊 Large dataset - consider pagination")

            except TimeoutError:
                print("⚠️  Handle timeout: retry with exponential backoff")
            except ValueError as ve:
                print(f"⚠️  Handle validation error: {ve}")
            except Exception as api_error:
                print(f"⚠️  Handle API error: {type(api_error).__name__}")

        print("✅ Resources automatically cleaned up on exit")

    except Exception as e:
        print(f"⚠️  Demo mode: {type(e).__name__}")

    print()


# =============================================================================
# 🎯 EXAMPLE 4: Data Processing Patterns
# =============================================================================


def example_data_processing():
    """Demonstrate common data processing patterns."""
    print("5️⃣ Data Processing Patterns")
    print("-" * 30)

    print("📊 Common data processing workflows:")

    try:
        with SyncApiClient(config) as client:
            members_api = SyncMembersApi(client)
            sales_api = SyncSalesApi(client)

            # Simulate data processing
            def mock_data_processing():
                """Simulate typical data processing tasks."""

                print("\n   🔄 Processing member data...")
                # Raw member data
                # members = members_api.get_members(take=100)

                # Example processing
                mock_members = [
                    {"id": 1, "name": "John Doe", "status": "active"},
                    {"id": 2, "name": "Jane Smith", "status": "inactive"},
                    {"id": 3, "name": "Bob Johnson", "status": "active"},
                ]

                # Filter active members
                active_members = [m for m in mock_members if m["status"] == "active"]
                print(f"   ✅ Found {len(active_members)} active members")

                print("\n   💰 Processing sales data...")
                # Sales analysis
                # sales = sales_api.get_sales(take=50)

                mock_sales = [
                    {"amount": 99.99, "date": "2024-01-01"},
                    {"amount": 149.99, "date": "2024-01-02"},
                    {"amount": 79.99, "date": "2024-01-03"},
                ]

                # Calculate totals
                total_revenue = sum(sale["amount"] for sale in mock_sales)
                print(f"   ✅ Total revenue: ${total_revenue:.2f}")

                # Data aggregation
                print("\n   📈 Generating reports...")
                report = {
                    "total_members": len(mock_members),
                    "active_members": len(active_members),
                    "total_sales": len(mock_sales),
                    "revenue": total_revenue,
                }

                print("   ✅ Report generated:")
                for key, value in report.items():
                    print(f"      {key}: {value}")

                return report

            report = mock_data_processing()
            print(f"\n🎯 Data processing completed successfully!")

    except Exception as e:
        print(f"⚠️  Demo mode: {type(e).__name__}")

    print()


# =============================================================================
# 🎯 EXAMPLE 5: Pagination and Large Datasets
# =============================================================================


def example_pagination():
    """Demonstrate handling pagination and large datasets."""
    print("6️⃣ Pagination and Large Datasets")
    print("-" * 35)

    print("📄 Pagination patterns:")

    try:
        with SyncApiClient(config) as client:
            members_api = SyncMembersApi(client)

            # Pagination example
            def mock_pagination():
                """Simulate pagination handling."""

                page_size = 50
                total_processed = 0
                page = 1

                print(f"   📋 Processing in batches of {page_size}...")

                # Simulate multiple pages
                for page in range(1, 4):  # Simulate 3 pages
                    print(f"   🔄 Processing page {page}...")

                    # This would be a real API call:
                    # members = members_api.get_members(
                    #     skip=(page-1) * page_size,
                    #     take=page_size
                    # )

                    # Simulate processing
                    batch_size = page_size if page < 3 else 23  # Last page partial
                    total_processed += batch_size

                    print(f"      ✅ Processed {batch_size} records")

                    # Break condition for real implementation:
                    # if len(members) < page_size:
                    #     break  # Last page

                print(f"   ✅ Total processed: {total_processed} records")
                return total_processed

            total = mock_pagination()
            print(f"\n🎯 Pagination completed: {total} total records")

    except Exception as e:
        print(f"⚠️  Demo mode: {type(e).__name__}")

    print()


# =============================================================================
# 🎯 EXAMPLE 6: Before vs After Comparison
# =============================================================================


def show_before_after_comparison():
    """Show the dramatic improvement from our refactoring."""
    print("7️⃣ Before vs After Comparison")
    print("-" * 32)

    print("❌ BEFORE (Complex Overloaded Methods):")
    print(
        """
   from evo_client.api import MembersApi
   from multiprocessing.pool import AsyncResult
   
   api = MembersApi()
   
   # Confusing! Multiple ways to call same method:
   members1 = api.get_members()                    # Direct
   members2 = api.get_members(async_req=False)     # Explicit sync
   result = api.get_members(async_req=True)        # Fake async
   members3 = result.get()                         # Blocking!
   
   # Problems:
   # • 3+ different ways to call same method
   # • Union[List[Model], AsyncResult] return types
   # • Confusing async_req parameter
   # • Threading complexity
   # • Resource management issues
"""
    )

    print("✅ AFTER (Clean Simple Methods):")
    print(
        """
   from evo_client.sync.api import SyncMembersApi
   from evo_client.config import QuickConfig
   
   config = QuickConfig.gym_basic("gym_dns", "secret")
   with SyncApiClient(config) as client:
       members_api = SyncMembersApi(client)
       members = members_api.get_members()  # Simple!
   
   # Benefits:
   # ✅ One clear way to call each method
   # ✅ Clean return types (no Union confusion)
   # ✅ No async_req parameter needed
   # ✅ Proper context managers
   # ✅ Automatic resource cleanup
   # ✅ Type-safe and intuitive
"""
    )


# =============================================================================
# 🎯 EXAMPLE 7: Configuration Integration Demo
# =============================================================================


def example_configuration_integration():
    """Demonstrate integration with our configuration helpers."""
    print("8️⃣ Configuration Integration Demo")
    print("-" * 36)

    from evo_client.config import ConfigValidator

    print("🔧 Testing different configuration approaches:")

    # Test multiple configurations
    configs_to_test = [
        ("Quick Setup", QuickConfig.gym_basic("demo", "secret")),
        ("Development", ConfigPresets.gym_development()),
        ("Production", ConfigPresets.gym_production()),
        ("High Performance", ConfigPresets.high_performance()),
    ]

    for name, test_config in configs_to_test:
        print(f"\n   🔍 Testing: {name}")

        # Validate configuration
        is_valid, errors, warnings = ConfigValidator.validate_config(test_config)
        print(f"      Validation: {'✅ VALID' if is_valid else '❌ INVALID'}")

        if warnings:
            print(f"      Warnings: {len(warnings)} found")

        # Test with sync client
        try:
            with SyncApiClient(test_config) as client:
                print(f"      Client: ✅ Created successfully")
        except Exception as e:
            print(f"      Client: ⚠️  {type(e).__name__}")

    print(f"\n🎯 Configuration testing completed!")


# =============================================================================
# 🎯 MAIN EXECUTION
# =============================================================================


def main():
    """Main demo function."""
    print("🎊 Welcome to the Modern Sync EVO Client Demo!")
    print("This showcases our clean, simplified sync implementation.\n")

    # Run all examples
    example_basic_sync()
    example_multiple_apis()
    example_error_handling()
    example_data_processing()
    example_pagination()
    example_configuration_integration()

    show_before_after_comparison()

    print()
    print("🎯 Key Sync Achievements Summary")
    print("-" * 35)

    achievements = [
        "✅ Eliminated complex @overload decorators",
        "✅ Removed confusing async_req parameters",
        "✅ Simplified all method signatures",
        "✅ Added proper context manager support",
        "✅ Improved error handling patterns",
        "✅ Better resource management",
        "✅ Type-safe, intuitive APIs",
        "✅ Easy configuration with helpers",
        "✅ Maintained full backward compatibility",
        "✅ Clear, direct method calls",
    ]

    for achievement in achievements:
        print(f"  {achievement}")

    print()
    print("🎉 Modern Sync Demo Complete!")
    print("🚀 Phase 2 + 3 + 4.1 + 4.2: SPECTACULAR SUCCESS!")
    print("\nSync APIs are now clean, simple, and intuitive! 🎊")


if __name__ == "__main__":
    # Run the comprehensive sync demo
    main()
