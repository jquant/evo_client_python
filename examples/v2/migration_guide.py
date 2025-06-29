#!/usr/bin/env python3
"""
🔄 EVO Client Migration Guide
============================

This guide shows how to migrate from the old confusing "bundler problem"
patterns to the new clean sync/async implementation.

🎯 MIGRATION PATHS:
1. Old Sync Code → New Sync Code (Easy!)
2. Old Fake Async → New Real Async (Better!)
3. Configuration Updates (Powerful!)

Usage:
    python examples/migration_guide.py
"""

import sys
import os
import asyncio

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

print("🔄 EVO Client Migration Guide")
print("=" * 35)
print()
print(
    "This guide helps you migrate from the old patterns to our new clean implementation."
)
print(
    "All old code continues to work (backward compatibility), but new patterns are better!"
)
print()

# =============================================================================
# 🎯 MIGRATION 1: Basic Sync API Usage
# =============================================================================


def migration_1_basic_sync():
    """Show migration from old sync to new sync patterns."""
    print("1️⃣ Migration 1: Basic Sync API Usage")
    print("-" * 40)

    print("❌ OLD WAY (Still works, but verbose):")
    print(
        """
   from evo_client import ApiClient, Configuration, MembersApi
   
   # Verbose configuration setup
   config = Configuration()
   config.host = "https://evo-integracao-api.w12app.com.br"
   config.username = "your_gym_dns" 
   config.password = "your_secret_key"
   
   # Manual client creation
   client = ApiClient(configuration=config)
   api = MembersApi(api_client=client)
   
   # Method call (works but verbose)
   members = api.get_members()
   
   # Manual cleanup required
   """
    )

    print("✅ NEW WAY (Recommended - Clean & Easy):")
    print(
        """
   from evo_client.sync import SyncApiClient
   from evo_client.sync.api import SyncMembersApi
   from evo_client.config import QuickConfig
   
   # Easy configuration
   config = QuickConfig.gym_basic("your_gym_dns", "your_secret_key")
   
   # Clean context manager pattern
   with SyncApiClient(config) as client:
       members_api = SyncMembersApi(client)
       members = members_api.get_members()  # Simple!
   # Automatic cleanup
   """
    )

    print("🎯 BENEFITS OF NEW WAY:")
    benefits = [
        "✅ One-line configuration with QuickConfig",
        "✅ Automatic resource management",
        "✅ Cleaner imports",
        "✅ Type-safe APIs",
        "✅ Better error handling",
    ]
    for benefit in benefits:
        print(f"   {benefit}")

    print()


# =============================================================================
# 🎯 MIGRATION 2: Configuration Setup
# =============================================================================


def migration_2_configuration():
    """Show migration from manual config to helper-based config."""
    print("2️⃣ Migration 2: Configuration Setup")
    print("-" * 38)

    print("❌ OLD WAY (Manual, error-prone):")
    print(
        """
   from evo_client import Configuration
   
   # Manual configuration - easy to make mistakes
   config = Configuration()
   config.host = "https://evo-integracao-api.w12app.com.br"
   config.username = "gym_dns"
   config.password = "secret_key"
   config.timeout = 60
   config.verify_ssl = True
   config.connection_pool_maxsize = 10
   # Easy to forget settings or make errors
   """
    )

    print("✅ NEW WAY (Helper-based, error-free):")
    print(
        """
   from evo_client.config import ConfigBuilder, ConfigPresets, QuickConfig
   
   # Option 1: Environment-based (production recommended)
   config = ConfigBuilder.from_env()  # Reads EVO_* variables
   
   # Option 2: Quick setup
   config = QuickConfig.gym_basic("gym_dns", "secret_key")
   
   # Option 3: Presets for common scenarios
   config = ConfigPresets.gym_development()  # Dev-friendly
   config = ConfigPresets.gym_production()   # Production-ready
   config = ConfigPresets.high_performance() # Bulk operations
   
   # Option 4: Factory methods
   config = ConfigBuilder.basic_auth(
       host="https://api.evo.com",
       username="gym_dns",
       password="secret_key"
   )
   """
    )

    print("🎯 CONFIGURATION HELPER BENEFITS:")
    benefits = [
        "✅ Environment variable automation",
        "✅ Preset configurations for common scenarios",
        "✅ Built-in validation and error checking",
        "✅ One-line setup in most cases",
        "✅ Production-ready defaults",
    ]
    for benefit in benefits:
        print(f"   {benefit}")

    print()


# =============================================================================
# 🎯 MIGRATION 3: Fake Async to Real Async
# =============================================================================


def migration_3_async():
    """Show migration from fake async to real async patterns."""
    print("3️⃣ Migration 3: Fake Async → Real Async")
    print("-" * 42)

    print("❌ OLD WAY (Confusing fake async):")
    print(
        """
   from evo_client.api import MembersApi
   from multiprocessing.pool import AsyncResult
   
   api = MembersApi()
   
   # Fake async - returns AsyncResult (threading)
   result = api.get_members(async_req=True)  # Confusing!
   
   # Blocking call defeats the purpose
   members = result.get()  # This blocks anyway!
   
   # Problems:
   # • Not real async (uses threading)
   # • Confusing AsyncResult return type
   # • Still blocks when you need the data
   # • Can't use with asyncio frameworks
   # • Resource leaks possible
   """
    )

    print("✅ NEW WAY (Real async with asyncio):")
    print(
        """
   import asyncio
   from evo_client.aio import AsyncApiClient
   from evo_client.aio.api import AsyncMembersApi
   from evo_client.config import ConfigPresets
   
   async def get_members_async():
       config = ConfigPresets.gym_development()
       config.username = "gym_dns"
       config.password = "secret_key"
       
       async with AsyncApiClient(config) as client:
           members_api = AsyncMembersApi(client)
           members = await members_api.get_members()  # Real async!
           return members
   
   # Run with asyncio
   members = asyncio.run(get_members_async())
   """
    )

    print("🎯 REAL ASYNC BENEFITS:")
    benefits = [
        "✅ True async/await with aiohttp",
        "✅ Real concurrent request handling",
        "✅ Works with asyncio frameworks (FastAPI, etc.)",
        "✅ Proper connection pooling",
        "✅ No threading complexity",
        "✅ Better resource management",
    ]
    for benefit in benefits:
        print(f"   {benefit}")

    print()


# =============================================================================
# 🎯 MIGRATION 4: Multiple API Usage
# =============================================================================


def migration_4_multiple_apis():
    """Show migration for using multiple APIs."""
    print("4️⃣ Migration 4: Multiple API Usage")
    print("-" * 37)

    print("❌ OLD WAY (Verbose, repetitive):")
    print(
        """
   from evo_client import ApiClient, Configuration
   from evo_client.api import MembersApi, SalesApi, ActivitiesApi
   
   # Manual setup for each
   config = Configuration()
   config.host = "https://evo-integracao-api.w12app.com.br"
   config.username = "gym_dns"
   config.password = "secret_key"
   
   client = ApiClient(configuration=config)
   
   # Create each API separately
   members_api = MembersApi(api_client=client)
   sales_api = SalesApi(api_client=client)
   activities_api = ActivitiesApi(api_client=client)
   
   # Use them
   members = members_api.get_members()
   sales = sales_api.get_sales()
   activities = activities_api.get_activities()
   
   # Manual cleanup
   """
    )

    print("✅ NEW WAY (Clean, organized):")
    print(
        """
   from evo_client.sync import SyncApiClient
   from evo_client.sync.api import SyncMembersApi, SyncSalesApi, SyncActivitiesApi
   from evo_client.config import QuickConfig
   
   # One-line configuration
   config = QuickConfig.gym_basic("gym_dns", "secret_key")
   
   # Clean context manager for all APIs
   with SyncApiClient(config) as client:
       # Create all APIs
       members_api = SyncMembersApi(client)
       sales_api = SyncSalesApi(client)
       activities_api = SyncActivitiesApi(client)
       
       # Use them cleanly
       members = members_api.get_members()
       sales = sales_api.get_sales()
       activities = activities_api.get_activities()
   # Automatic cleanup for all
   """
    )

    print("🎯 MULTIPLE API BENEFITS:")
    benefits = [
        "✅ Shared client and connection pool",
        "✅ Automatic resource management for all APIs",
        "✅ Clean organization",
        "✅ Type-safe imports",
        "✅ Consistent patterns",
    ]
    for benefit in benefits:
        print(f"   {benefit}")

    print()


# =============================================================================
# 🎯 MIGRATION 5: Error Handling
# =============================================================================


def migration_5_error_handling():
    """Show migration for error handling patterns."""
    print("5️⃣ Migration 5: Error Handling")
    print("-" * 33)

    print("❌ OLD WAY (Complex, error-prone):")
    print(
        """
   from evo_client.api import MembersApi
   from multiprocessing.pool import AsyncResult
   import requests
   
   api = MembersApi()
   
   try:
       # Sync call
       members = api.get_members()
   except requests.RequestException as e:
       print(f"Network error: {e}")
   except Exception as e:
       print(f"Unknown error: {e}")
   
   # Async call error handling is more complex
   try:
       result = api.get_members(async_req=True)
       members = result.get(timeout=30)  # May timeout
   except Exception as e:
       print(f"Async error: {e}")
   """
    )

    print("✅ NEW WAY (Clean, comprehensive):")
    print(
        """
   from evo_client.sync import SyncApiClient
   from evo_client.sync.api import SyncMembersApi
   from evo_client.config import QuickConfig, ConfigValidator
   import requests
   
   # Validate configuration first
   config = QuickConfig.gym_basic("gym_dns", "secret_key")
   is_valid, errors, warnings = ConfigValidator.validate_config(config)
   
   if not is_valid:
       print(f"Config errors: {errors}")
       return
   
   # Clean error handling
   try:
       with SyncApiClient(config) as client:
           members_api = SyncMembersApi(client)
           members = members_api.get_members()
           
   except requests.Timeout:
       print("Request timed out - check network")
   except requests.ConnectionError:
       print("Connection failed - check host/credentials")
   except requests.HTTPError as e:
       print(f"API error: {e.response.status_code}")
   except Exception as e:
       print(f"Unexpected error: {e}")
   """
    )

    print("🎯 ERROR HANDLING BENEFITS:")
    benefits = [
        "✅ Configuration validation before use",
        "✅ Clear, specific exception types",
        "✅ Automatic resource cleanup on errors",
        "✅ Better error messages",
        "✅ Consistent patterns across sync/async",
    ]
    for benefit in benefits:
        print(f"   {benefit}")

    print()


# =============================================================================
# 🎯 MIGRATION 6: Async Concurrent Requests
# =============================================================================


def migration_6_concurrent():
    """Show migration to real concurrent async requests."""
    print("6️⃣ Migration 6: Concurrent Requests")
    print("-" * 37)

    print("❌ OLD WAY (Fake concurrency with threading):")
    print(
        """
   from evo_client.api import MembersApi, SalesApi
   from multiprocessing.pool import AsyncResult
   
   members_api = MembersApi()
   sales_api = SalesApi()
   
   # Fake async - uses threading
   members_result = members_api.get_members(async_req=True)
   sales_result = sales_api.get_sales(async_req=True)
   
   # Still have to block and wait
   members = members_result.get()  # Blocking
   sales = sales_result.get()      # Blocking
   
   # Problems:
   # • Threading overhead
   # • Global Interpreter Lock limits performance
   # • Resource management issues
   # • Not truly concurrent
   """
    )

    print("✅ NEW WAY (True async concurrency):")
    print(
        """
   import asyncio
   from evo_client.aio import AsyncApiClient
   from evo_client.aio.api import AsyncMembersApi, AsyncSalesApi
   from evo_client.config import ConfigPresets
   
   async def get_data_concurrently():
       config = ConfigPresets.high_performance()
       config.username = "gym_dns"
       config.password = "secret_key"
       
       async with AsyncApiClient(config) as client:
           members_api = AsyncMembersApi(client)
           sales_api = AsyncSalesApi(client)
           
           # TRUE concurrency with asyncio.gather
           members, sales = await asyncio.gather(
               members_api.get_members(),
               sales_api.get_sales()
           )
           
           return members, sales
   
   # Run truly concurrent requests
   members, sales = asyncio.run(get_data_concurrently())
   """
    )

    print("🎯 CONCURRENT REQUEST BENEFITS:")
    benefits = [
        "✅ True async concurrency (no GIL issues)",
        "✅ Shared connection pool for efficiency",
        "✅ Much faster for multiple requests",
        "✅ Natural asyncio.gather() patterns",
        "✅ Better resource utilization",
    ]
    for benefit in benefits:
        print(f"   {benefit}")

    print()


# =============================================================================
# 🎯 STEP-BY-STEP MIGRATION PLAN
# =============================================================================


def show_migration_plan():
    """Provide a step-by-step migration plan."""
    print("7️⃣ Step-by-Step Migration Plan")
    print("-" * 35)

    print("🎯 RECOMMENDED MIGRATION STEPS:")
    print()

    steps = [
        (
            "Step 1",
            "Update Configuration",
            [
                "Replace manual Configuration() with ConfigBuilder.from_env()",
                "Or use QuickConfig.gym_basic() for simple setups",
                "Or use ConfigPresets for common scenarios",
                "Add configuration validation",
            ],
        ),
        (
            "Step 2",
            "Migrate Sync Code",
            [
                "Replace 'from evo_client.api import XxxApi'",
                "With 'from evo_client.sync.api import SyncXxxApi'",
                "Add context managers: 'with SyncApiClient(config) as client:'",
                "Remove async_req=True parameters",
            ],
        ),
        (
            "Step 3",
            "Migrate Async Code",
            [
                "Replace fake async patterns",
                "Use 'from evo_client.aio.api import AsyncXxxApi'",
                "Add proper async/await patterns",
                "Use asyncio.gather() for concurrent requests",
            ],
        ),
        (
            "Step 4",
            "Update Error Handling",
            [
                "Add configuration validation",
                "Use specific exception types",
                "Implement proper timeout handling",
                "Add retry logic where appropriate",
            ],
        ),
        (
            "Step 5",
            "Test & Optimize",
            [
                "Validate all functionality works",
                "Measure performance improvements",
                "Optimize connection pool sizes",
                "Update documentation and examples",
            ],
        ),
    ]

    for step_num, step_name, step_details in steps:
        print(f"📋 {step_num}: {step_name}")
        for detail in step_details:
            print(f"   • {detail}")
        print()


# =============================================================================
# 🎯 QUICK REFERENCE TABLE
# =============================================================================


def show_quick_reference():
    """Show a quick reference table for common patterns."""
    print("8️⃣ Quick Reference Table")
    print("-" * 26)

    print("📚 COMMON PATTERN MIGRATIONS:")
    print()

    patterns = [
        (
            "Import APIs",
            "from evo_client.api import MembersApi",
            "from evo_client.sync.api import SyncMembersApi",
        ),
        (
            "Configuration",
            "config = Configuration(); config.host = ...",
            "config = QuickConfig.gym_basic('dns', 'key')",
        ),
        (
            "Client Creation",
            "client = ApiClient(configuration=config)",
            "with SyncApiClient(config) as client:",
        ),
        (
            "API Instance",
            "api = MembersApi(api_client=client)",
            "api = SyncMembersApi(client)",
        ),
        (
            "Sync Call",
            "members = api.get_members()",
            "members = api.get_members()  # Same!",
        ),
        (
            "Fake Async",
            "result = api.get_members(async_req=True); members = result.get()",
            "members = await api.get_members()  # Real async!",
        ),
        (
            "Async Import",
            "# No real async before",
            "from evo_client.aio.api import AsyncMembersApi",
        ),
        (
            "Async Client",
            "# No real async before",
            "async with AsyncApiClient(config) as client:",
        ),
    ]

    print(f"{'Old Pattern':<35} → {'New Pattern'}")
    print("-" * 80)

    for description, old, new in patterns:
        print(f"\n{description}:")
        print(f"❌ {old}")
        print(f"✅ {new}")


# =============================================================================
# 🎯 MAIN EXECUTION
# =============================================================================


def main():
    """Main migration guide function."""
    print("🎊 Welcome to the EVO Client Migration Guide!")
    print("This guide helps you transition to our clean new patterns.\n")

    # Show all migration patterns
    migration_1_basic_sync()
    migration_2_configuration()
    migration_3_async()
    migration_4_multiple_apis()
    migration_5_error_handling()
    migration_6_concurrent()

    show_migration_plan()
    show_quick_reference()

    print()
    print("🎯 Migration Summary")
    print("-" * 20)

    summary = [
        "✅ All old code continues to work (backward compatible)",
        "✅ New patterns are cleaner and more powerful",
        "✅ Configuration helpers eliminate common errors",
        "✅ Real async enables true concurrency",
        "✅ Better error handling and resource management",
        "✅ Type-safe APIs reduce bugs",
        "✅ Step-by-step migration minimizes risk",
        "✅ Comprehensive examples available",
    ]

    for item in summary:
        print(f"  {item}")

    print()
    print("🎉 Migration Guide Complete!")
    print("🚀 Start with Step 1 and migrate at your own pace!")
    print("\n💡 Remember: Old code keeps working, so you can migrate gradually! 🎊")


if __name__ == "__main__":
    # Run the comprehensive migration guide
    main()
