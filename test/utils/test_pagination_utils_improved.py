"""Tests for improved pagination utilities."""

import pytest
import time
from typing import List
from unittest.mock import Mock, patch, call

from evo_client.utils.pagination_utils import (
    RateLimiter,
    RetryHandler,
    ApiCallExecutor,
    PaginatedApiCaller,
    PaginationConfig,
    RetryConfig,
    PaginationResult,
    create_paginated_caller,
    paginated_api_call,
)
from evo_client.exceptions.api_exceptions import ApiException


class TestPaginationConfig:
    """Test pagination configuration validation."""

    def test_valid_config(self):
        config = PaginationConfig(
            page_size=25,
            max_retries=3,
            base_delay=2.0,
            pagination_type="page_page_size",
        )
        assert config.page_size == 25
        assert config.max_retries == 3
        assert config.base_delay == 2.0
        assert config.pagination_type == "page_page_size"

    def test_invalid_pagination_type(self):
        with pytest.raises(ValueError, match="pagination_type must be"):
            PaginationConfig(pagination_type="invalid_type")

    def test_invalid_page_size(self):
        with pytest.raises(ValueError, match="page_size must be positive"):
            PaginationConfig(page_size=0)

    def test_invalid_max_retries(self):
        with pytest.raises(ValueError, match="max_retries must be non-negative"):
            PaginationConfig(max_retries=-1)


class TestRetryConfig:
    """Test retry configuration validation."""

    def test_valid_config(self):
        config = RetryConfig(max_retries=3, base_delay=1.0, exponential_backoff=False)
        assert config.max_retries == 3
        assert config.base_delay == 1.0
        assert config.exponential_backoff is False

    def test_invalid_max_retries(self):
        with pytest.raises(ValueError, match="max_retries must be non-negative"):
            RetryConfig(max_retries=-1)

    def test_invalid_base_delay(self):
        with pytest.raises(ValueError, match="base_delay must be non-negative"):
            RetryConfig(base_delay=-1.0)


class TestPaginationResult:
    """Test pagination result functionality."""

    def test_successful_result(self):
        result = PaginationResult(
            data=[1, 2, 3], success=True, total_requests=2, total_retries=0
        )
        assert result.data == [1, 2, 3]
        assert result.success is True
        assert result.has_errors is False
        assert result.total_requests == 2

    def test_failed_result(self):
        result = PaginationResult(
            data=[1, 2],
            success=False,
            error_message="API Error",
            total_requests=1,
            total_retries=3,
        )
        assert result.data == [1, 2]
        assert result.success is False
        assert result.has_errors is True
        assert result.error_message == "API Error"


class TestRateLimiter:
    """Test rate limiter functionality."""

    def test_initialization(self):
        limiter = RateLimiter(max_requests=10, time_window=30)
        assert limiter.max_requests == 10
        assert limiter.time_window == 30
        assert limiter.requests == []

    def test_invalid_initialization(self):
        with pytest.raises(ValueError, match="max_requests must be positive"):
            RateLimiter(max_requests=0)

        with pytest.raises(ValueError, match="time_window must be positive"):
            RateLimiter(time_window=0)

    def test_acquire_under_limit(self):
        limiter = RateLimiter(max_requests=5, time_window=60)

        # Should acquire immediately for first few requests
        limiter.acquire()
        limiter.acquire()
        limiter.acquire()

        assert len(limiter.requests) == 3

    @patch("time.sleep")
    @patch("time.time")
    def test_acquire_over_limit(self, mock_time, mock_sleep):
        # Mock time progression
        mock_time.side_effect = [0, 0, 0, 0, 10, 70]  # Sequence of time calls

        limiter = RateLimiter(max_requests=2, time_window=60)

        # Fill up the rate limit
        limiter.acquire()  # time=0
        limiter.acquire()  # time=0

        # This should trigger rate limiting
        limiter.acquire()  # time=0, should sleep for full window

        # Verify sleep was called with correct duration
        mock_sleep.assert_called_once_with(60.0)  # First request at 0 + 60 - 0 = 60

    def test_reset(self):
        limiter = RateLimiter()
        limiter.acquire()
        limiter.acquire()

        assert len(limiter.requests) == 2

        limiter.reset()
        assert len(limiter.requests) == 0


class TestRetryHandler:
    """Test retry handler functionality."""

    def test_extract_retry_after_found(self):
        handler = RetryHandler(RetryConfig())
        error_msg = "Rate limit exceeded. Retry-After: 30 seconds"

        delay = handler.extract_retry_after(error_msg)
        assert delay == 30.0

    def test_extract_retry_after_not_found(self):
        handler = RetryHandler(RetryConfig())
        error_msg = "Generic error message"

        delay = handler.extract_retry_after(error_msg)
        assert delay == 1.0

    def test_compute_backoff_delay_exponential(self):
        config = RetryConfig(base_delay=2.0, exponential_backoff=True)
        handler = RetryHandler(config)
        exception = Exception("Generic error")

        # Test exponential backoff: base_delay * (2 ** (attempt - 1))
        assert handler.compute_backoff_delay(1, exception) == 2.0  # 2 * 2^0
        assert handler.compute_backoff_delay(2, exception) == 4.0  # 2 * 2^1
        assert handler.compute_backoff_delay(3, exception) == 8.0  # 2 * 2^2

    def test_compute_backoff_delay_linear(self):
        config = RetryConfig(base_delay=3.0, exponential_backoff=False)
        handler = RetryHandler(config)
        exception = Exception("Generic error")

        # Test linear backoff (constant delay)
        assert handler.compute_backoff_delay(1, exception) == 3.0
        assert handler.compute_backoff_delay(2, exception) == 3.0
        assert handler.compute_backoff_delay(3, exception) == 3.0

    def test_compute_backoff_delay_rate_limit(self):
        config = RetryConfig(base_delay=1.0)
        handler = RetryHandler(config)

        # Mock the extract_retry_after method
        handler.extract_retry_after = Mock(return_value=5.0)

        exception = Exception("429 Too Many Requests")
        delay = handler.compute_backoff_delay(1, exception)

        # Should use the larger of backoff delay and retry-after
        assert delay == 5.0
        handler.extract_retry_after.assert_called_once_with("429 Too Many Requests")


class TestApiCallExecutor:
    """Test API call executor functionality."""

    def test_successful_call(self):
        mock_rate_limiter = Mock()
        mock_retry_handler = Mock()
        mock_retry_handler.config = RetryConfig(max_retries=3)

        executor = ApiCallExecutor(
            rate_limiter=mock_rate_limiter, retry_handler=mock_retry_handler
        )

        mock_api_func = Mock(return_value="success")

        result = executor.execute_with_retry(
            mock_api_func, "test context", param1="value1"
        )

        assert result == "success"
        mock_rate_limiter.acquire.assert_called_once()
        mock_api_func.assert_called_once_with(param1="value1")

    @patch("time.sleep")
    def test_retry_on_failure(self, mock_sleep):
        mock_rate_limiter = Mock()
        mock_retry_handler = Mock()
        mock_retry_handler.config = RetryConfig(max_retries=3)
        mock_retry_handler.compute_backoff_delay.side_effect = [1.0, 2.0, 4.0]

        executor = ApiCallExecutor(
            rate_limiter=mock_rate_limiter, retry_handler=mock_retry_handler
        )

        # Mock function that fails twice then succeeds
        mock_api_func = Mock(
            side_effect=[
                ApiException("First failure"),
                ApiException("Second failure"),
                "success",
            ]
        )

        result = executor.execute_with_retry(mock_api_func, "test context")

        assert result == "success"
        assert mock_rate_limiter.acquire.call_count == 3
        assert mock_api_func.call_count == 3
        assert mock_sleep.call_count == 2
        mock_sleep.assert_has_calls([call(1.0), call(2.0)])

    @patch("time.sleep")
    def test_max_retries_exceeded(self, mock_sleep):
        mock_rate_limiter = Mock()
        mock_retry_handler = Mock()
        mock_retry_handler.config = RetryConfig(max_retries=2)
        mock_retry_handler.compute_backoff_delay.return_value = 1.0

        executor = ApiCallExecutor(
            rate_limiter=mock_rate_limiter, retry_handler=mock_retry_handler
        )

        mock_api_func = Mock(side_effect=ApiException("Always fails"))

        with pytest.raises(ApiException, match="Always fails"):
            executor.execute_with_retry(mock_api_func, "test context")

        assert mock_rate_limiter.acquire.call_count == 2
        assert mock_api_func.call_count == 2
        # Verify sleep was called for retry delay
        mock_sleep.assert_called_once_with(1.0)


class TestPaginatedApiCaller:
    """Test paginated API caller functionality."""

    def test_build_pagination_params_skip_take(self):
        caller = PaginatedApiCaller()
        config = PaginationConfig(page_size=10, pagination_type="skip_take")

        params = caller._build_pagination_params(0, config)
        assert params == {"take": 10, "skip": 0}

        params = caller._build_pagination_params(2, config)
        assert params == {"take": 10, "skip": 20}

    def test_build_pagination_params_page_page_size(self):
        caller = PaginatedApiCaller()
        config = PaginationConfig(page_size=15, pagination_type="page_page_size")

        params = caller._build_pagination_params(0, config)
        assert params == {"page": 0, "page_size": 15}

        params = caller._build_pagination_params(3, config)
        assert params == {"page": 3, "page_size": 15}

    @patch("time.sleep")
    def test_fetch_all_pages_single_page(self, mock_sleep):
        mock_executor = Mock()
        mock_executor.execute_with_retry.return_value = [1, 2, 3, 4, 5]

        caller = PaginatedApiCaller(executor=mock_executor)
        config = PaginationConfig(page_size=10, post_request_delay=0.1)

        mock_api_func = Mock()

        result = caller.fetch_all_pages(
            mock_api_func, config, branch_id="test_branch", extra_param="value"
        )

        assert result.success is True
        assert result.data == [1, 2, 3, 4, 5]
        assert result.total_requests == 1

        # Verify the executor was called with correct parameters
        mock_executor.execute_with_retry.assert_called_once()
        call_args = mock_executor.execute_with_retry.call_args

        # call_args is (args, kwargs) where:
        # args[0] = api_func, args[1] = context string
        # kwargs contains the actual function parameters
        assert call_args[0][0] == mock_api_func  # api_func
        assert call_args[0][1].startswith("unknown_function page 0")  # context string
        assert call_args[1]["extra_param"] == "value"  # kwargs
        assert call_args[1]["take"] == 10
        assert call_args[1]["skip"] == 0

        mock_sleep.assert_called_once_with(0.1)

    @patch("time.sleep")
    def test_fetch_all_pages_multiple_pages(self, mock_sleep):
        mock_executor = Mock()
        # Simulate 3 pages: full, full, partial
        mock_executor.execute_with_retry.side_effect = [
            [1, 2, 3, 4, 5],  # Page 0: 5 items (page_size=5, so continue)
            [6, 7, 8, 9, 10],  # Page 1: 5 items (continue)
            [11, 12],  # Page 2: 2 items (< page_size, so stop)
        ]

        caller = PaginatedApiCaller(executor=mock_executor)
        config = PaginationConfig(page_size=5, post_request_delay=0.0)

        mock_api_func = Mock()

        result = caller.fetch_all_pages(mock_api_func, config, branch_id="test")

        assert result.success is True
        assert result.data == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        assert result.total_requests == 3
        assert mock_executor.execute_with_retry.call_count == 3

    @patch("time.sleep")
    def test_fetch_all_pages_empty_response(self, mock_sleep):
        mock_executor = Mock()
        mock_executor.execute_with_retry.return_value = []

        caller = PaginatedApiCaller(executor=mock_executor)
        # Use config with no delays to speed up test
        config = PaginationConfig(post_request_delay=0.0)
        mock_api_func = Mock()

        result = caller.fetch_all_pages(mock_api_func, config, branch_id="test")

        assert result.success is True
        assert result.data == []
        assert result.total_requests == 1
        # Should not sleep since post_request_delay=0.0
        mock_sleep.assert_not_called()

    @patch("time.sleep")
    def test_fetch_all_pages_non_list_response(self, mock_sleep):
        mock_executor = Mock()
        mock_executor.execute_with_retry.return_value = {"single": "object"}

        caller = PaginatedApiCaller(executor=mock_executor)
        # Use config with no delays to speed up test
        config = PaginationConfig(post_request_delay=0.0)
        mock_api_func = Mock()

        result = caller.fetch_all_pages(mock_api_func, config, branch_id="test")

        assert result.success is True
        assert result.data == [{"single": "object"}]
        assert result.total_requests == 1
        # Should not sleep since post_request_delay=0.0
        mock_sleep.assert_not_called()


class TestFactoryFunctions:
    """Test factory and backward compatibility functions."""

    def test_create_paginated_caller(self):
        caller = create_paginated_caller(
            max_requests_per_minute=30, max_retries=3, base_delay=2.0
        )

        assert isinstance(caller, PaginatedApiCaller)
        assert isinstance(caller.executor.rate_limiter, RateLimiter)
        assert isinstance(caller.executor.retry_handler, RetryHandler)

        # Check configuration
        assert caller.executor.rate_limiter.max_requests == 30
        assert caller.executor.retry_handler.config.max_retries == 3
        assert caller.executor.retry_handler.config.base_delay == 2.0

    def test_paginated_api_call_backward_compatibility(self):
        """Test that the old paginated_api_call function still works."""

        # Create a mock API function that returns data
        call_count = 0

        def mock_api_func(**kwargs):
            nonlocal call_count
            call_count += 1

            # Return paginated data based on skip parameter
            skip = kwargs.get("skip", 0)
            if skip == 0:
                return [1, 2, 3]  # First page
            elif skip == 3:
                return [4, 5]  # Second page (partial)
            else:
                return []  # No more data

        result = paginated_api_call(
            mock_api_func,
            page_size=3,
            max_retries=2,
            base_delay=0.1,  # Small delay for testing
            supports_pagination=True,
            pagination_type="skip_take",
            branch_id="test_branch",
            post_request_delay=0.0,  # No delay for testing
            extra_param="test_value",
        )

        # Verify the result
        assert result == [1, 2, 3, 4, 5]
        assert call_count == 2  # Two pages fetched


class TestIntegration:
    """Integration tests combining multiple components."""

    @patch("time.sleep")
    def test_full_integration_with_retry_and_pagination(self, mock_sleep):
        """Test a complete scenario with rate limiting, retries, and pagination."""

        # Create a real PaginatedApiCaller with minimal delays for testing
        rate_limiter = RateLimiter(max_requests=5, time_window=60)
        retry_handler = RetryHandler(RetryConfig(max_retries=2, base_delay=0.1))
        executor = ApiCallExecutor(rate_limiter, retry_handler)
        caller = PaginatedApiCaller(executor)

        config = PaginationConfig(
            page_size=3, post_request_delay=0.0  # No delay for testing
        )

        # Mock API function that fails once then returns paginated data
        call_count = 0

        def mock_api_func(**kwargs):
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

        result = caller.fetch_all_pages(
            mock_api_func, config, branch_id="integration_test"
        )

        # Verify the result
        assert result.success is True
        assert result.data == [1, 2, 3, 4, 5]
        assert result.total_requests == 2  # Two successful pages

        # Verify retry was attempted (sleep called for the first failure)
        mock_sleep.assert_called_once_with(0.1)

        # Verify we made the expected number of API calls (1 failed + 2 successful)
        assert call_count == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
