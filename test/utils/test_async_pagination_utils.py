"""Tests for async pagination utilities."""

import pytest
from typing import List
from unittest.mock import AsyncMock, Mock, patch

from evo_client.utils.async_pagination_utils import (
    AsyncRateLimiter,
    AsyncRetryHandler,
    AsyncApiCallExecutor,
    AsyncPaginatedApiCaller,
    ConcurrentPaginationManager,
    create_async_paginated_caller,
)
from evo_client.utils.pagination_utils import (
    PaginationConfig,
    RetryConfig,
)
from evo_client.exceptions.api_exceptions import ApiException


class TestAsyncRateLimiter:
    """Test async rate limiter functionality."""

    def test_initialization(self):
        limiter = AsyncRateLimiter(max_requests=10, time_window=30)
        assert limiter.max_requests == 10
        assert limiter.time_window == 30
        assert limiter.requests == []

    def test_invalid_initialization(self):
        with pytest.raises(ValueError, match="max_requests must be positive"):
            AsyncRateLimiter(max_requests=0)

        with pytest.raises(ValueError, match="time_window must be positive"):
            AsyncRateLimiter(time_window=0)

    @pytest.mark.asyncio
    async def test_acquire_under_limit(self):
        limiter = AsyncRateLimiter(max_requests=5, time_window=60)

        # Should acquire immediately for first few requests
        await limiter.acquire()
        await limiter.acquire()
        await limiter.acquire()

        assert len(limiter.requests) == 3

    @pytest.mark.asyncio
    @patch("asyncio.sleep")
    @patch("time.time")
    async def test_acquire_over_limit(self, mock_time, mock_sleep):
        # Mock time progression
        mock_time.side_effect = [0, 0, 0, 0, 10, 70]
        mock_sleep.return_value = None  # AsyncMock for asyncio.sleep

        limiter = AsyncRateLimiter(max_requests=2, time_window=60)

        # Fill up the rate limit
        await limiter.acquire()  # time=0
        await limiter.acquire()  # time=0

        # This should trigger rate limiting
        await limiter.acquire()  # time=0, should sleep

        # Verify sleep was called
        mock_sleep.assert_called_once_with(60.0)

    @pytest.mark.asyncio
    async def test_reset(self):
        limiter = AsyncRateLimiter()
        await limiter.acquire()
        await limiter.acquire()

        assert len(limiter.requests) == 2

        await limiter.reset()
        assert len(limiter.requests) == 0


class TestAsyncRetryHandler:
    """Test async retry handler functionality."""

    def test_extract_retry_after_found(self):
        handler = AsyncRetryHandler(RetryConfig())
        error_msg = "Rate limit exceeded. Retry-After: 30 seconds"

        delay = handler.extract_retry_after(error_msg)
        assert delay == 30.0

    def test_extract_retry_after_not_found(self):
        handler = AsyncRetryHandler(RetryConfig())
        error_msg = "Generic error message"

        delay = handler.extract_retry_after(error_msg)
        assert delay == 1.0

    def test_compute_backoff_delay_exponential(self):
        config = RetryConfig(base_delay=2.0, exponential_backoff=True)
        handler = AsyncRetryHandler(config)
        exception = Exception("Generic error")

        # Test exponential backoff
        assert handler.compute_backoff_delay(1, exception) == 2.0
        assert handler.compute_backoff_delay(2, exception) == 4.0
        assert handler.compute_backoff_delay(3, exception) == 8.0

    def test_compute_backoff_delay_rate_limit(self):
        config = RetryConfig(base_delay=1.0)
        handler = AsyncRetryHandler(config)

        # Mock the extract_retry_after method
        handler.extract_retry_after = Mock(return_value=5.0)

        exception = Exception("429 Too Many Requests")
        delay = handler.compute_backoff_delay(1, exception)

        assert delay == 5.0
        handler.extract_retry_after.assert_called_once_with("429 Too Many Requests")


class TestAsyncApiCallExecutor:
    """Test async API call executor functionality."""

    @pytest.mark.asyncio
    async def test_successful_call(self):
        mock_rate_limiter = AsyncMock()
        mock_retry_handler = Mock()
        mock_retry_handler.config = RetryConfig(max_retries=3)

        executor = AsyncApiCallExecutor(
            rate_limiter=mock_rate_limiter, retry_handler=mock_retry_handler
        )

        async def mock_api_func(**kwargs):
            return "success"

        result = await executor.execute_with_retry(
            mock_api_func, "test context", param1="value1"
        )

        assert result == "success"
        mock_rate_limiter.acquire.assert_called_once()

    @pytest.mark.asyncio
    @patch("asyncio.sleep")
    async def test_retry_on_failure(self, mock_sleep):
        mock_rate_limiter = AsyncMock()
        mock_retry_handler = Mock()
        mock_retry_handler.config = RetryConfig(max_retries=3)
        mock_retry_handler.compute_backoff_delay.side_effect = [0.1, 0.2, 0.4]

        executor = AsyncApiCallExecutor(
            rate_limiter=mock_rate_limiter, retry_handler=mock_retry_handler
        )

        call_count = 0

        async def failing_then_success(**kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                raise ApiException(f"Failure {call_count}")
            return "success"

        result = await executor.execute_with_retry(failing_then_success, "test context")

        assert result == "success"
        assert mock_rate_limiter.acquire.call_count == 3
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_max_retries_exceeded(self):
        mock_rate_limiter = AsyncMock()
        mock_retry_handler = Mock()
        mock_retry_handler.config = RetryConfig(max_retries=2)
        mock_retry_handler.compute_backoff_delay.return_value = 0.1

        executor = AsyncApiCallExecutor(
            rate_limiter=mock_rate_limiter, retry_handler=mock_retry_handler
        )

        async def always_fails(**kwargs):
            raise ApiException("Always fails")

        with pytest.raises(ApiException, match="Always fails"):
            await executor.execute_with_retry(always_fails, "test context")

        assert mock_rate_limiter.acquire.call_count == 2


class TestAsyncPaginatedApiCaller:
    """Test async paginated API caller functionality."""

    def test_build_pagination_params_skip_take(self):
        caller = AsyncPaginatedApiCaller()
        config = PaginationConfig(page_size=10, pagination_type="skip_take")

        params = caller._build_pagination_params(0, config)
        assert params == {"take": 10, "skip": 0}

        params = caller._build_pagination_params(2, config)
        assert params == {"take": 10, "skip": 20}

    @pytest.mark.asyncio
    @patch("asyncio.sleep")
    async def test_fetch_all_pages_single_page(self, mock_sleep):
        mock_executor = AsyncMock()
        mock_executor.execute_with_retry = AsyncMock(return_value=[1, 2, 3, 4, 5])

        caller = AsyncPaginatedApiCaller(executor=mock_executor)
        config = PaginationConfig(page_size=10, post_request_delay=0.1)

        async def mock_api_func(**kwargs):
            return [1, 2, 3, 4, 5]

        result = await caller.fetch_all_pages(
            mock_api_func, config, branch_id="test_branch", extra_param="value"
        )

        assert result.success is True
        assert result.data == [1, 2, 3, 4, 5]
        assert result.total_requests == 1

    @pytest.mark.asyncio
    @patch("asyncio.sleep")
    async def test_fetch_all_pages_multiple_pages(self, mock_sleep):
        mock_executor = AsyncMock()
        mock_executor.execute_with_retry = AsyncMock(
            side_effect=[
                [1, 2, 3, 4, 5],  # Page 0: full page
                [6, 7, 8, 9, 10],  # Page 1: full page
                [11, 12],  # Page 2: partial page (stop)
            ]
        )

        caller = AsyncPaginatedApiCaller(executor=mock_executor)
        config = PaginationConfig(page_size=5, post_request_delay=0.0)

        async def mock_api_func(**kwargs) -> List:
            return []  # Mock will handle the return values via side_effect

        result = await caller.fetch_all_pages(mock_api_func, config, branch_id="test")

        assert result.success is True
        assert result.data == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        assert result.total_requests == 3

    @pytest.mark.asyncio
    async def test_fetch_all_pages_api_error(self):
        mock_executor = AsyncMock()
        mock_retry_handler = Mock()
        mock_retry_handler.config = Mock()
        mock_retry_handler.config.max_retries = 3
        mock_executor.retry_handler = mock_retry_handler
        mock_executor.execute_with_retry = AsyncMock(
            side_effect=ApiException("API failed")
        )

        caller = AsyncPaginatedApiCaller(executor=mock_executor)

        async def mock_api_func(**kwargs) -> List:
            return []  # This won't be called due to the exception

        result = await caller.fetch_all_pages(mock_api_func, branch_id="test")

        assert result.success is False
        assert result.error_message == "API failed"
        assert result.data == []

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        caller = AsyncPaginatedApiCaller()

        async with caller as ctx_caller:
            assert ctx_caller is caller


class TestFactoryFunctions:
    """Test async factory and utility functions."""

    def test_create_async_paginated_caller(self):
        caller = create_async_paginated_caller(
            max_requests_per_minute=30, max_retries=3, base_delay=2.0
        )

        assert isinstance(caller, AsyncPaginatedApiCaller)
        assert isinstance(caller.executor.rate_limiter, AsyncRateLimiter)
        assert isinstance(caller.executor.retry_handler, AsyncRetryHandler)

        # Check configuration
        assert caller.executor.rate_limiter.max_requests == 30
        assert caller.executor.retry_handler.config.max_retries == 3
        assert caller.executor.retry_handler.config.base_delay == 2.0


class TestConcurrentPaginationManager:
    """Test concurrent pagination manager functionality."""

    @pytest.mark.asyncio
    async def test_fetch_multiple_branches_success(self):
        # Use mocks instead of real objects for speed
        mock_rate_limiter = AsyncMock()
        mock_retry_handler = Mock()
        mock_retry_handler.config = RetryConfig(max_retries=1, base_delay=0.01)

        # Create mock executor that uses mocked components
        mock_executor = AsyncMock()
        mock_executor.rate_limiter = mock_rate_limiter
        mock_executor.retry_handler = mock_retry_handler

        # Mock the execute_with_retry to return data directly
        async def mock_execute_with_retry(api_func, context, *args, **kwargs):
            return await api_func(*args, **kwargs)

        mock_executor.execute_with_retry.side_effect = mock_execute_with_retry

        manager = ConcurrentPaginationManager(
            max_concurrent_operations=2,
            global_rate_limiter=mock_rate_limiter,
        )

        # Patch the AsyncApiCallExecutor to return our mock
        with patch(
            "evo_client.utils.async_pagination_utils.AsyncApiCallExecutor",
            return_value=mock_executor,
        ):

            async def mock_api_func(**kwargs):
                # Extract branch_id from kwargs since it's passed there
                branch_id = kwargs.get("branch_id", "unknown")
                if branch_id == "branch1":
                    return [
                        {"id": 1, "branch": branch_id},
                        {"id": 2, "branch": branch_id},
                    ]
                elif branch_id == "branch2":
                    return [{"id": 3, "branch": branch_id}]
                else:
                    return []

            branch_configs = [
                {"branch_id": "branch1", "filter": "active"},
                {"branch_id": "branch2", "filter": "inactive"},
            ]

            # Use fast configuration to reduce test time
            fast_config = PaginationConfig(
                page_size=10, post_request_delay=0.0, max_retries=1, base_delay=0.01
            )
            results = await manager.fetch_multiple_branches(
                mock_api_func, branch_configs, fast_config
            )

            assert len(results) == 2
            assert "branch1" in results
            assert "branch2" in results
            assert results["branch1"].success is True
            assert results["branch2"].success is True
            assert len(results["branch1"].data) == 2
            assert len(results["branch2"].data) == 1

    @pytest.mark.asyncio
    async def test_fetch_multiple_branches_with_failure(self):
        # Use mocks instead of real objects for speed
        mock_rate_limiter = AsyncMock()
        mock_retry_handler = Mock()
        mock_retry_handler.config = RetryConfig(max_retries=1, base_delay=0.01)

        # Create mock executor that uses mocked components
        mock_executor = AsyncMock()
        mock_executor.rate_limiter = mock_rate_limiter
        mock_executor.retry_handler = mock_retry_handler

        # Mock the execute_with_retry to either return data or raise exception
        async def mock_execute_with_retry(api_func, context, *args, **kwargs):
            try:
                return await api_func(*args, **kwargs)
            except Exception as e:
                # For failing branch, simulate retry exhaustion
                raise e

        mock_executor.execute_with_retry.side_effect = mock_execute_with_retry

        manager = ConcurrentPaginationManager(
            max_concurrent_operations=3,
            global_rate_limiter=mock_rate_limiter,
        )

        # Patch the AsyncApiCallExecutor to return our mock
        with patch(
            "evo_client.utils.async_pagination_utils.AsyncApiCallExecutor",
            return_value=mock_executor,
        ):

            async def mock_api_func(**kwargs):
                branch_id = kwargs.get("branch_id", "unknown")
                if branch_id == "failing_branch":
                    raise ApiException("Branch API failed")
                return [{"id": 1, "branch": branch_id}]

            branch_configs = [
                {"branch_id": "good_branch"},
                {"branch_id": "failing_branch"},
            ]

            # Use fast configuration to reduce test time
            fast_config = PaginationConfig(
                page_size=10,
                max_retries=1,  # Reduce retries for faster tests
                base_delay=0.01,  # Very short delay
                post_request_delay=0.0,
            )

            results = await manager.fetch_multiple_branches(
                mock_api_func, branch_configs, fast_config
            )

            # Should have results for both branches - one successful, one failed
            assert len(results) == 2
            assert "good_branch" in results
            assert "failing_branch" in results

            # Good branch should succeed
            assert results["good_branch"].success is True
            assert len(results["good_branch"].data) == 1

            # Failing branch should have success=False
            assert results["failing_branch"].success is False
            assert results["failing_branch"].error_message == "Branch API failed"


class TestAsyncIntegration:
    """Integration tests for async pagination utilities."""

    @pytest.mark.asyncio
    @patch("asyncio.sleep")
    async def test_full_async_integration_with_retry_and_pagination(self, mock_sleep):
        """Test a complete async scenario with rate limiting, retries, and pagination."""

        # Create a real AsyncPaginatedApiCaller with fast configurations for testing
        rate_limiter = AsyncRateLimiter(
            max_requests=10, time_window=1
        )  # More requests in shorter window
        retry_handler = AsyncRetryHandler(
            RetryConfig(max_retries=2, base_delay=0.01)
        )  # Shorter delays
        executor = AsyncApiCallExecutor(rate_limiter, retry_handler)
        caller = AsyncPaginatedApiCaller(executor)

        config = PaginationConfig(
            page_size=3, post_request_delay=0.0
        )  # No delay between requests

        # Mock API function that fails once then returns paginated data
        call_count = 0

        async def mock_api_func(**kwargs):
            nonlocal call_count
            call_count += 1

            # Fail on first call, then succeed
            if call_count == 1:
                raise ApiException("Temporary failure")

            # Return different data based on pagination
            skip = kwargs.get("skip", 0)
            if skip == 0:
                return [1, 2, 3]  # First page (full)
            elif skip == 3:
                return [4, 5]  # Second page (partial, should stop)
            else:
                return []  # No more data

        result = await caller.fetch_all_pages(
            mock_api_func, config, branch_id_logging="integration_test"
        )

        # Verify the result
        assert result.success is True
        assert result.data == [1, 2, 3, 4, 5]
        assert result.total_requests == 2  # Two successful pages

        # Verify we made the expected number of API calls (1 failed + 2 successful)
        assert call_count == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
