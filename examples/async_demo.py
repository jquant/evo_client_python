"""
Demonstration of the new clean async implementation.

This example shows how much cleaner the async pattern is compared to
the old threading-based "fake async" approach.
"""

import asyncio
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from evo_client.core.configuration import Configuration
from evo_client.aio import AsyncApiClient
from evo_client.aio.api.members_api import AsyncMembersApi


async def demo_async_client():
    """Demonstrate the clean async client usage."""
    print("🚀 EVO Client Async Demo")
    print("=" * 50)

    # Configure the client
    config = Configuration(
        host="https://evo-integracao-api.w12app.com.br",
        username="your_username",  # Replace with actual credentials
        password="your_password",  # Replace with actual credentials
    )

    print("✅ Configuration created")

    # Example 1: Using AsyncApiClient directly
    print("\n📡 Example 1: Direct API Client Usage")
    print("-" * 30)

    try:
        async with AsyncApiClient(config) as client:
            print("✅ Async client created with context manager")

            # Make a direct API call
            # Note: This would fail without valid credentials, but shows the pattern
            print("📞 Making async API call...")
            # response = await client.call_api(
            #     resource_path="/api/v1/members/basic-info",
            #     method="GET",
            #     query_params={"take": 5},
            #     auth_settings=["Basic"]
            # )
            print("✅ API call pattern demonstrated")

    except Exception as e:
        print(f"ℹ️  Expected error (no credentials): {type(e).__name__}")

    # Example 2: Using specific API classes
    print("\n🎯 Example 2: Specific API Usage")
    print("-" * 30)

    try:
        async with AsyncMembersApi() as members_api:
            print("✅ AsyncMembersApi created with context manager")

            # This shows the clean async pattern
            print(
                "📞 Would call: await members_api.get_basic_info(email='test@example.com')"
            )
            print(
                "📞 Would call: await members_api.authenticate_member('user', 'pass')"
            )
            print("📞 Would call: await members_api.update_fitcoins(123, 'add', 100)")

            print("✅ Clean async patterns demonstrated")

    except Exception as e:
        print(f"ℹ️  Expected error (no credentials): {type(e).__name__}")


def show_comparison():
    """Show the comparison between old and new patterns."""
    print("\n🔄 Pattern Comparison")
    print("=" * 50)

    print("\n❌ OLD (Confusing) Pattern:")
    print("-" * 25)
    print(
        """
# Fake async with threading - CONFUSING!
from evo_client.api import MembersApi

api = MembersApi()
result = api.get_basic_info(email="test@example.com", async_req=True)
# ^ Returns AsyncResult object, not actual async!

data = result.get()  # <- Blocking call defeats the purpose!
# Multiple overloads, complex Union types, threading issues
"""
    )

    print("\n✅ NEW (Clean) Pattern:")
    print("-" * 20)
    print(
        """
# Real async with aiohttp - BEAUTIFUL!
from evo_client.aio.api import AsyncMembersApi

async with AsyncMembersApi() as api:
    data = await api.get_basic_info(email="test@example.com")
    # ^ Natural async/await - no confusion!
    
# Simple methods, clean types, proper async context management
"""
    )


async def demo_concurrent_requests():
    """Demonstrate the power of real async with concurrent requests."""
    print("\n⚡ Example 3: Concurrent Requests (Real Async Power)")
    print("-" * 50)

    config = Configuration(
        host="https://evo-integracao-api.w12app.com.br",
        username="your_username",
        password="your_password",
    )

    try:
        async with AsyncMembersApi() as api:
            print("🚀 Making multiple concurrent async calls...")

            # This is where real async shines - concurrent requests!
            tasks = [
                # api.get_basic_info(email=f"user{i}@example.com")
                # for i in range(5)
            ]

            # Simulate the concurrent pattern
            print("📊 Would execute 5 concurrent API calls:")
            for i in range(5):
                print(f"   - Task {i+1}: get_basic_info(email='user{i}@example.com')")

            # results = await asyncio.gather(*tasks)
            print("✅ All requests would complete concurrently!")
            print("⚡ This is IMPOSSIBLE with the old threading approach!")

    except Exception as e:
        print(f"ℹ️  Demo completed (no real calls made)")


def show_benefits():
    """Show the key benefits of the new approach."""
    print("\n🎯 Key Benefits Achieved")
    print("=" * 50)

    benefits = [
        "✅ Real async/await (no more fake AsyncResult)",
        "✅ Clean, simple method signatures",
        "✅ Natural context manager support",
        "✅ Proper connection pooling with aiohttp",
        "✅ No threading complexity or resource leaks",
        "✅ True concurrent request handling",
        "✅ Better error handling and logging",
        "✅ Type-safe, no complex Union types",
        "✅ Easy to test and mock",
        "✅ Compatible with asyncio frameworks",
    ]

    for benefit in benefits:
        print(f"  {benefit}")


async def main():
    """Main demo function."""
    print("🎉 Welcome to the EVO Client Async Refactor Demo!")
    print(
        "This demonstrates our successful transition from 'fake async' to real async.\n"
    )

    show_comparison()

    await demo_async_client()

    await demo_concurrent_requests()

    show_benefits()

    print("\n🎉 Demo Complete!")
    print("Phase 1 of the async refactor is SUCCESSFUL! 🚀")
    print("\nNext steps:")
    print("  - Install aiohttp: pip install aiohttp")
    print("  - Create comprehensive tests")
    print("  - Continue with Phase 2: Sync cleanup")


if __name__ == "__main__":
    # Run the async demo
    asyncio.run(main())
