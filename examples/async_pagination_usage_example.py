"""
Examples demonstrating how to use the async pagination utilities.

This shows the benefits of the async refactored code:
1. Better performance with async/await patterns
2. Concurrent pagination for multiple branches
3. Proper resource management with rate limiting
4. Easy testing and mocking
5. Backward compatibility with async API
"""

import asyncio
from datetime import datetime
from dataclasses import asdict

from evo_client.utils.async_pagination_utils import (
    AsyncPaginatedApiCaller,
    ConcurrentPaginationManager,
    create_async_paginated_caller,
    async_paginated_api_call,
)
from evo_client.utils.pagination_utils import PaginationConfig


async def example_1_basic_async_usage():
    """Basic async usage with default configuration."""
    print("=== Example 1: Basic Async Usage ===")

    # Simple usage with factory function
    caller = create_async_paginated_caller(
        max_requests_per_minute=30,  # Conservative rate limiting
        max_retries=3,
        base_delay=1.0,
    )

    # Mock async API function for demonstration
    async def get_members_api(**kwargs):
        """Simulated async API function that returns member data."""
        skip = kwargs.get("skip", 0)
        take = kwargs.get("take", 50)

        # Simulate different pages
        if skip == 0:
            return [{"id": i, "name": f"Member {i}"} for i in range(1, 51)]
        elif skip == 50:
            return [
                {"id": i, "name": f"Member {i}"} for i in range(51, 76)
            ]  # Partial page
        else:
            return []  # No more data

    # Fetch all members
    result = await caller.fetch_all_pages(
        get_members_api, branch_id="branch_001", extra_filter="active_only"
    )

    print(f"Success: {result.success}")
    print(f"Total items: {len(result.data)}")
    print(f"Total requests: {result.total_requests}")
    print(f"Has errors: {result.has_errors}")
    print()


async def example_2_concurrent_branches():
    """Demonstrate concurrent pagination for multiple branches."""
    print("=== Example 2: Concurrent Branch Processing ===")

    # Create concurrent manager
    manager = ConcurrentPaginationManager(
        max_concurrent_operations=3,  # Process 3 branches at once
    )

    # Mock API function that responds differently per branch
    async def get_branch_data(**kwargs):
        """Simulated API that returns different data per branch."""
        branch_id = kwargs.get("branch_id", "unknown")
        filter_type = kwargs.get("filter", "all")

        print(f"Fetching data for branch {branch_id} with filter {filter_type}")

        # Simulate branch-specific data
        if branch_id == "branch_001":
            return [
                {"id": i, "branch": branch_id, "type": "premium"} for i in range(1, 11)
            ]
        elif branch_id == "branch_002":
            return [
                {"id": i, "branch": branch_id, "type": "standard"} for i in range(1, 6)
            ]
        elif branch_id == "branch_003":
            return [
                {"id": i, "branch": branch_id, "type": "basic"} for i in range(1, 21)
            ]
        else:
            return []

    # Define branch configurations
    branch_configs = [
        {"branch_id": "branch_001", "filter": "premium"},
        {"branch_id": "branch_002", "filter": "standard"},
        {"branch_id": "branch_003", "filter": "basic"},
    ]

    config = PaginationConfig(page_size=50, post_request_delay=0.1)

    # Fetch data for all branches concurrently
    results = await manager.fetch_multiple_branches(
        get_branch_data, branch_configs, config
    )

    print(f"Processed {len(results)} branches:")
    for branch_id, result in results.items():
        status = "✅ Success" if result.success else "❌ Failed"
        print(f"  {branch_id}: {status} - {len(result.data)} items")
    print()


async def example_3_async_context_manager():
    """Using async context manager for resource management."""
    print("=== Example 3: Async Context Manager ===")

    async def fetch_data(**kwargs):
        """Simple async API mock."""
        return [{"id": 1, "data": "sample"}]

    # Use async context manager
    async with create_async_paginated_caller() as caller:
        result = await caller.fetch_all_pages(fetch_data, branch_id="ctx_test")
        print(f"Context manager result: {len(result.data)} items")
    print()


async def example_4_async_backward_compatibility():
    """Using the async backward compatibility function."""
    print("=== Example 4: Async Backward Compatibility ===")

    async def legacy_async_api(**kwargs):
        """Legacy async API function format."""
        skip = kwargs.get("skip", 0)
        take = kwargs.get("take", 50)

        if skip == 0:
            return [f"async_item_{i}" for i in range(1, 26)]  # 25 items
        else:
            return []  # Single page

    # Use the async backward compatibility function
    result = await async_paginated_api_call(
        legacy_async_api,
        page_size=25,
        max_retries=3,
        base_delay=0.5,
        supports_pagination=True,
        pagination_type="skip_take",
        branch_id="async_legacy_branch",
        post_request_delay=0.0,
        legacy_param="async_style",
    )

    print(f"Async legacy API result: {result}")
    print(f"Total items: {len(result)}")
    print()


async def example_5_error_handling():
    """Demonstrate async error handling and recovery."""
    print("=== Example 5: Async Error Handling ===")

    call_count = 0

    async def failing_then_recovering_api(**kwargs):
        """Async API that fails initially then recovers."""
        nonlocal call_count
        call_count += 1

        # Fail on first two calls
        if call_count <= 2:
            raise Exception(f"Async temporary failure #{call_count}")

        # Then succeed
        skip = kwargs.get("skip", 0)
        if skip == 0:
            return [{"id": 1, "data": "async_recovered"}]
        else:
            return []

    caller = create_async_paginated_caller(max_retries=3, base_delay=0.1)
    result = await caller.fetch_all_pages(
        failing_then_recovering_api, branch_id="async_recovery_test"
    )

    print(f"Async recovery test success: {result.success}")
    print(f"Data recovered: {result.data}")
    print(f"Total API calls made: {call_count}")
    print()


async def example_6_performance_comparison():
    """Compare performance of sync vs async approaches."""
    print("=== Example 6: Performance Benefits ===")

    # Mock API with artificial delay
    async def slow_api(**kwargs):
        """API with simulated network delay."""
        await asyncio.sleep(0.1)  # Simulate 100ms API call
        return [{"id": 1, "timestamp": datetime.now().isoformat()}]

    # Test concurrent processing
    branch_configs = [{"branch_id": f"perf_branch_{i}"} for i in range(5)]

    manager = ConcurrentPaginationManager(max_concurrent_operations=5)

    start_time = datetime.now()
    results = await manager.fetch_multiple_branches(slow_api, branch_configs)
    end_time = datetime.now()

    duration = (end_time - start_time).total_seconds()
    print(f"Processed {len(results)} branches concurrently in {duration:.2f}s")
    print(f"Average time per branch: {duration / len(results):.2f}s")
    print("(Sequential processing would take ~0.5s total)")
    print()


async def main():
    """Run all async pagination examples."""
    print("🚀 Async Pagination Utilities Examples")
    print("=" * 50)
    print()

    # Run all examples
    await example_1_basic_async_usage()
    await example_2_concurrent_branches()
    await example_3_async_context_manager()
    await example_4_async_backward_compatibility()
    await example_5_error_handling()
    await example_6_performance_comparison()

    print("✅ All async examples completed successfully!")
    print()
    print("Key Benefits of Async Pagination Utilities:")
    print("• Non-blocking I/O for better performance")
    print("• Concurrent processing of multiple branches")
    print("• Proper resource management with async context managers")
    print("• Same configuration and error handling as sync version")
    print("• Easy migration from sync to async")
    print("• Backward compatibility with existing async APIs")


if __name__ == "__main__":
    asyncio.run(main())
