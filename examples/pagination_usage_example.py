"""
Examples demonstrating how to use the improved pagination utilities.

This shows the benefits of the refactored code:
1. Better type safety and configuration
2. Easier testing and mocking
3. More flexible rate limiting and retry strategies
4. Better error handling and reporting
"""

from datetime import datetime
from dataclasses import asdict

# Add the project root to Python path
from evo_client.utils.pagination_utils import (
    PaginatedApiCaller,
    PaginationConfig,
    RetryConfig,
    RateLimiter,
    RetryHandler,
    ApiCallExecutor,
    create_paginated_caller,
    paginated_api_call,  # Backward compatibility
)


def example_1_basic_usage():
    """Basic usage with default configuration."""
    print("=== Example 1: Basic Usage ===")

    # Simple usage with factory function
    caller = create_paginated_caller(
        max_requests_per_minute=30,  # Conservative rate limiting
        max_retries=3,
        base_delay=1.0,
    )

    # Mock API function for demonstration
    def get_members_api(**kwargs):
        """Simulated API function that returns member data."""
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
    result = caller.fetch_all_pages(
        get_members_api, branch_id="branch_001", extra_filter="active_only"
    )

    print(f"Success: {result.success}")
    print(f"Total items: {len(result.data)}")
    print(f"Total requests: {result.total_requests}")
    print(f"Has errors: {result.has_errors}")
    print()


def example_2_custom_configuration():
    """Advanced usage with custom configuration."""
    print("=== Example 2: Custom Configuration ===")

    # Create custom configuration for different scenarios
    bulk_config = PaginationConfig(
        page_size=100,  # Larger pages for bulk operations
        max_retries=5,  # More retries for critical operations
        base_delay=2.0,  # Longer delays between retries
        post_request_delay=0.5,  # Delay between successful requests
        pagination_type="page_page_size",  # Different pagination style
    )

    # Custom rate limiter for high-volume operations
    conservative_limiter = RateLimiter(max_requests=20, time_window=60)

    # Custom retry handler with linear backoff
    linear_retry = RetryHandler(
        RetryConfig(
            max_retries=3,
            base_delay=1.5,
            exponential_backoff=False,  # Linear instead of exponential
        )
    )

    # Combine everything
    executor = ApiCallExecutor(
        rate_limiter=conservative_limiter, retry_handler=linear_retry
    )
    caller = PaginatedApiCaller(executor=executor, default_config=bulk_config)

    def get_sales_data(**kwargs):
        """Simulated sales API function."""
        page = kwargs.get("page", 0)
        page_size = kwargs.get("page_size", 100)

        if page == 0:
            return [{"sale_id": i, "amount": i * 10.0} for i in range(1, 101)]
        elif page == 1:
            return [
                {"sale_id": i, "amount": i * 10.0} for i in range(101, 151)
            ]  # Partial
        else:
            return []

    result = caller.fetch_all_pages(
        get_sales_data,
        config=bulk_config,  # Override default config
        branch_id="sales_branch",
        date_filter="2024-01",
    )

    print(f"Bulk operation success: {result.success}")
    print(f"Total sales records: {len(result.data)}")
    print(f"Configuration used: {asdict(bulk_config)}")
    print()


def example_3_error_handling():
    """Demonstrating error handling and recovery."""
    print("=== Example 3: Error Handling ===")

    # Create caller with minimal retries for demonstration
    caller = create_paginated_caller(max_retries=2, base_delay=0.1)

    call_count = 0

    def failing_api(**kwargs):
        """API that fails initially then recovers."""
        nonlocal call_count
        call_count += 1

        # Fail on first two calls
        if call_count <= 2:
            raise Exception(f"Temporary failure #{call_count}")

        # Then succeed
        skip = kwargs.get("skip", 0)
        if skip == 0:
            return [{"id": 1, "data": "recovered"}]
        else:
            return []

    result = caller.fetch_all_pages(failing_api, branch_id="recovery_test")

    print(f"Recovery test success: {result.success}")
    print(f"Data recovered: {result.data}")
    print(f"Total API calls made: {call_count}")
    print()


def example_4_backward_compatibility():
    """Using the old API for backward compatibility."""
    print("=== Example 4: Backward Compatibility ===")

    def legacy_api(**kwargs):
        """Legacy API function format."""
        skip = kwargs.get("skip", 0)
        take = kwargs.get("take", 50)

        if skip == 0:
            return [f"legacy_item_{i}" for i in range(1, 26)]  # 25 items
        else:
            return []  # Single page

    # Use the old function signature
    result = paginated_api_call(
        legacy_api,
        page_size=25,
        max_retries=3,
        base_delay=1.0,
        supports_pagination=True,
        pagination_type="skip_take",
        branch_id="legacy_branch",
        post_request_delay=0.0,
        legacy_param="old_style",
    )

    print(f"Legacy API result: {result}")
    print(f"Total items: {len(result)}")
    print()


def example_5_real_world_scenario():
    """Real-world scenario with member data fetching."""
    print("=== Example 5: Real-World Member Fetching ===")

    # Configuration for member data fetching
    member_config = PaginationConfig(
        page_size=50,  # Reasonable page size
        max_retries=3,  # Standard retry count
        base_delay=1.0,  # Standard delay
        post_request_delay=0.2,  # Small delay to be API-friendly
        supports_pagination=True,
        pagination_type="skip_take",
    )

    # Create specialized caller for member operations
    member_caller = create_paginated_caller(
        max_requests_per_minute=40, max_retries=3, base_delay=1.0  # Within API limits
    )

    def fetch_active_members(**kwargs):
        """Simulate fetching active members from different branches."""
        skip = kwargs.get("skip", 0)
        take = kwargs.get("take", 50)
        branch_filter = kwargs.get("branch_id", "all")

        # Simulate realistic member data
        start_id = skip + 1
        end_id = min(skip + take, 150)  # Simulate 150 total members

        if start_id > 150:
            return []

        members = []
        for i in range(start_id, end_id + 1):
            member = {
                "id": i,
                "name": f"Member {i:03d}",
                "email": f"member{i:03d}@example.com",
                "branch_id": branch_filter,
                "active": True,
                "join_date": f"2024-01-{(i % 28) + 1:02d}",
            }
            members.append(member)

        return members

    # Fetch all active members
    result = member_caller.fetch_all_pages(
        fetch_active_members,
        config=member_config,
        branch_id="main_branch",
        status_filter="active",
    )

    if result.success:
        print(f"Successfully fetched {len(result.data)} members")
        print(f"Made {result.total_requests} API requests")
        print(f"First member: {result.data[0] if result.data else 'None'}")
        print(f"Last member: {result.data[-1] if result.data else 'None'}")
    else:
        print(f"Failed to fetch members: {result.error_message}")
        print(f"Partial data: {len(result.data)} members")

    # Demonstrate error checking
    if result.has_errors:
        print(f"Warning: Operation completed with errors: {result.error_message}")

    print()


def example_6_rate_limiting_demo():
    """Demonstrate rate limiting behavior."""
    print("=== Example 6: Rate Limiting Demo ===")

    # Create rate limiter with very low limits for demonstration
    demo_limiter = RateLimiter(
        max_requests=3, time_window=5
    )  # 3 requests per 5 seconds

    print("Making rapid requests to demonstrate rate limiting...")

    for i in range(5):
        print(f"Request {i+1} - acquiring rate limit permission...")
        demo_limiter.acquire()
        print(f"Request {i+1} - granted at {datetime.now().strftime('%H:%M:%S')}")

    print("Rate limiting demo completed!")
    print()


if __name__ == "__main__":
    """Run all examples to demonstrate the improved pagination utilities."""

    print("🚀 Improved Pagination Utilities Examples")
    print("=" * 50)
    print()

    # Run all examples
    example_1_basic_usage()
    example_2_custom_configuration()
    example_3_error_handling()
    example_4_backward_compatibility()
    example_5_real_world_scenario()

    # Note: Commented out rate limiting demo to avoid delays in automated runs
    # example_6_rate_limiting_demo()

    print("✅ All examples completed successfully!")
    print()
    print("Key Benefits of the Improved Pagination Utilities:")
    print("• Better type safety with dataclasses and protocols")
    print("• Easier testing with dependency injection")
    print("• Configurable rate limiting and retry strategies")
    print("• Comprehensive error handling and reporting")
    print("• Backward compatibility with existing code")
    print("• Clear separation of concerns for maintainability")
