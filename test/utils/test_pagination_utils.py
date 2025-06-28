"""Tests for pagination_utils module."""

import pytest
import time
from unittest.mock import Mock, patch, MagicMock
from src.evo_client.utils.pagination_utils import (
    RateLimiter,
    extract_retry_after,
    compute_backoff_delay,
    fetch_for_unit,
    paginated_api_call,
)
from src.evo_client.exceptions.api_exceptions import ApiException


class TestRateLimiter:
    """Test suite for RateLimiter class."""

    def test_initialization(self):
        """Test RateLimiter initialization with default and custom parameters."""
        # Default initialization
        limiter = RateLimiter()
        assert limiter.max_requests == 40
        assert limiter.time_window == 60
        assert limiter.requests == []

        # Custom initialization
        limiter = RateLimiter(max_requests=10, time_window=30)
        assert limiter.max_requests == 10
        assert limiter.time_window == 30

    def test_acquire_within_limits(self):
        """Test that acquire works normally when within rate limits."""
        limiter = RateLimiter(max_requests=5, time_window=60)

        # Should not block when within limits
        start_time = time.time()
        limiter.acquire()
        end_time = time.time()

        assert end_time - start_time < 0.1  # Should be nearly instant
        assert len(limiter.requests) == 1

    def test_acquire_rate_limit_reached(self):
        """Test that acquire blocks when rate limit is reached."""
        limiter = RateLimiter(max_requests=2, time_window=60)

        # Fill up the rate limiter
        limiter.acquire()
        limiter.acquire()

        # Mock time.sleep to avoid actual waiting in tests
        with patch("time.sleep") as mock_sleep, patch(
            "src.evo_client.utils.pagination_utils.logger"
        ) as mock_logger:

            # This should trigger rate limiting
            limiter.acquire()

            # Should have called sleep
            mock_sleep.assert_called()
            mock_logger.warning.assert_called()

    def test_old_requests_cleanup(self):
        """Test that old requests are properly cleaned up."""
        limiter = RateLimiter(max_requests=5, time_window=1)  # 1 second window

        # Add some requests
        with patch("time.time") as mock_time:
            mock_time.return_value = 100.0
            limiter.acquire()

            # Advance time beyond window
            mock_time.return_value = 102.0
            limiter.acquire()

            # Should have cleaned up old requests
            assert len(limiter.requests) == 1

    def test_thread_safety(self):
        """Test that RateLimiter is thread-safe."""
        limiter = RateLimiter(max_requests=10, time_window=60)

        # This is a basic test - proper thread safety testing would be more complex
        # but checking that the lock exists and acquire method completes
        assert hasattr(limiter, "_lock")
        limiter.acquire()
        assert len(limiter.requests) == 1


class TestExtractRetryAfter:
    """Test suite for extract_retry_after function."""

    def test_extract_retry_after_present(self):
        """Test extracting retry-after value when present in error message."""
        error_msg = "Rate limit exceeded. Retry-After: 30 seconds"
        result = extract_retry_after(error_msg)
        assert result == 30.0

    def test_extract_retry_after_different_format(self):
        """Test extracting retry-after value in different formats."""
        error_msg = "Error 429. Retry-After: 15"
        result = extract_retry_after(error_msg)
        assert result == 15.0

    def test_extract_retry_after_not_present(self):
        """Test default value when retry-after is not present."""
        error_msg = "Some other error message"
        result = extract_retry_after(error_msg)
        assert result == 1.0

    def test_extract_retry_after_invalid_format(self):
        """Test handling of invalid retry-after format."""
        error_msg = "Retry-After: invalid_number"
        result = extract_retry_after(error_msg)
        assert result == 1.0

    def test_extract_retry_after_multiple_numbers(self):
        """Test that first number is extracted when multiple numbers present."""
        error_msg = "Retry-After: 45 and then 60 more seconds"
        result = extract_retry_after(error_msg)
        assert result == 45.0

    def test_extract_retry_after_empty_after_colon(self):
        """Test handling when nothing follows Retry-After:."""
        error_msg = "Retry-After:"
        result = extract_retry_after(error_msg)
        assert result == 1.0


class TestComputeBackoffDelay:
    """Test suite for compute_backoff_delay function."""

    def test_exponential_backoff_normal_error(self):
        """Test exponential backoff for normal errors."""
        base_delay = 2.0
        exception = Exception("Normal error")

        # First attempt
        delay = compute_backoff_delay(base_delay, 1, exception)
        assert delay == 2.0  # 2 * 2^0

        # Second attempt
        delay = compute_backoff_delay(base_delay, 2, exception)
        assert delay == 4.0  # 2 * 2^1

        # Third attempt
        delay = compute_backoff_delay(base_delay, 3, exception)
        assert delay == 8.0  # 2 * 2^2

    def test_rate_limit_error_with_retry_after(self):
        """Test that rate limit errors respect Retry-After header."""
        base_delay = 1.0
        exception = Exception("HTTP 429: Rate limit exceeded. Retry-After: 10")

        delay = compute_backoff_delay(base_delay, 1, exception)
        assert delay == 10.0  # Should use Retry-After value instead of exponential

    def test_rate_limit_error_without_retry_after(self):
        """Test rate limit error without Retry-After header."""
        base_delay = 1.0
        exception = Exception("HTTP 429: Too Many Requests")

        delay = compute_backoff_delay(base_delay, 2, exception)
        # Should use max of exponential backoff and default retry-after (1.0)
        assert delay == max(2.0, 1.0)  # 2.0

    def test_too_many_requests_error(self):
        """Test 'Too Many Requests' error handling."""
        base_delay = 0.5
        exception = Exception("Too Many Requests error")

        delay = compute_backoff_delay(base_delay, 3, exception)
        # Should use max of exponential backoff (2.0) and default retry-after (1.0)
        assert delay == max(2.0, 1.0)  # 2.0


class TestFetchForUnit:
    """Test suite for fetch_for_unit function."""

    def test_successful_single_page_fetch(self):
        """Test successful fetch with single page of results."""
        mock_api_func = Mock(return_value=["item1", "item2", "item3"])

        with patch("time.sleep"), patch(
            "src.evo_client.utils.pagination_utils.RateLimiter"
        ) as mock_rate_limiter:
            mock_rate_limiter.return_value.acquire = Mock()

            result = fetch_for_unit(
                api_func=mock_api_func,
                kwargs={"param": "value"},
                page_size=10,
                max_retries=3,
                base_delay=1.0,
                supports_pagination=True,
                pagination_type="skip_take",
            )

        assert result == ["item1", "item2", "item3"]
        mock_api_func.assert_called_once_with(
            param="value", async_req=False, take=10, skip=0
        )

    def test_successful_multiple_page_fetch(self):
        """Test successful fetch with multiple pages."""
        # First call returns full page, second returns partial page
        mock_api_func = Mock(
            side_effect=[
                ["item1", "item2", "item3", "item4", "item5"],  # Page 0
                ["item6", "item7"],  # Page 1 (partial, indicates end)
            ]
        )

        with patch("time.sleep"), patch(
            "src.evo_client.utils.pagination_utils.RateLimiter"
        ) as mock_rate_limiter:
            mock_rate_limiter.return_value.acquire = Mock()

            result = fetch_for_unit(
                api_func=mock_api_func,
                kwargs={},
                page_size=5,
                max_retries=3,
                base_delay=1.0,
                supports_pagination=True,
                pagination_type="skip_take",
            )

        assert result == ["item1", "item2", "item3", "item4", "item5", "item6", "item7"]
        assert mock_api_func.call_count == 2

    def test_page_page_size_pagination(self):
        """Test pagination with page/page_size parameters."""
        mock_api_func = Mock(return_value=["item1", "item2"])

        with patch("time.sleep"), patch(
            "src.evo_client.utils.pagination_utils.RateLimiter"
        ) as mock_rate_limiter:
            mock_rate_limiter.return_value.acquire = Mock()

            result = fetch_for_unit(
                api_func=mock_api_func,
                kwargs={"filter": "active"},
                page_size=5,
                max_retries=3,
                base_delay=1.0,
                supports_pagination=True,
                pagination_type="page_page_size",
            )

        mock_api_func.assert_called_once_with(
            filter="active", async_req=False, page=0, page_size=5
        )

    def test_no_pagination_support(self):
        """Test fetch when pagination is not supported."""
        mock_api_func = Mock(return_value=["item1", "item2", "item3"])

        with patch("time.sleep"), patch(
            "src.evo_client.utils.pagination_utils.RateLimiter"
        ) as mock_rate_limiter:
            mock_rate_limiter.return_value.acquire = Mock()

            result = fetch_for_unit(
                api_func=mock_api_func,
                kwargs={"param": "value"},
                page_size=10,
                max_retries=3,
                base_delay=1.0,
                supports_pagination=False,
                pagination_type="skip_take",
            )

        # Should not add pagination parameters
        mock_api_func.assert_called_once_with(param="value", async_req=False)

    def test_retry_on_exception(self):
        """Test retry behavior on exceptions."""
        mock_api_func = Mock(
            side_effect=[
                Exception("Temporary failure"),
                Exception("Another failure"),
                ["success"],
            ]
        )

        with patch("time.sleep"), patch(
            "src.evo_client.utils.pagination_utils.RateLimiter"
        ) as mock_rate_limiter, patch(
            "src.evo_client.utils.pagination_utils.logger"
        ) as mock_logger:
            mock_rate_limiter.return_value.acquire = Mock()

            result = fetch_for_unit(
                api_func=mock_api_func,
                kwargs={},
                page_size=10,
                max_retries=3,
                base_delay=0.1,
                supports_pagination=True,
                pagination_type="skip_take",
            )

        assert result == ["success"]
        assert mock_api_func.call_count == 3
        mock_logger.warning.assert_called()

    def test_max_retries_exceeded(self):
        """Test behavior when max retries are exceeded."""
        mock_api_func = Mock(side_effect=Exception("Persistent failure"))

        with patch("time.sleep"), patch(
            "src.evo_client.utils.pagination_utils.RateLimiter"
        ) as mock_rate_limiter, patch(
            "src.evo_client.utils.pagination_utils.logger"
        ) as mock_logger:
            mock_rate_limiter.return_value.acquire = Mock()

            with pytest.raises(ValueError) as exc_info:
                fetch_for_unit(
                    api_func=mock_api_func,
                    kwargs={},
                    page_size=10,
                    max_retries=2,
                    base_delay=0.1,
                    supports_pagination=True,
                    pagination_type="skip_take",
                )

        assert "Max retries reached" in str(exc_info.value)
        assert mock_api_func.call_count == 2
        mock_logger.error.assert_called()

    def test_empty_result_handling(self):
        """Test handling of empty results."""
        mock_api_func = Mock(return_value=[])

        with patch("time.sleep"), patch(
            "src.evo_client.utils.pagination_utils.RateLimiter"
        ) as mock_rate_limiter:
            mock_rate_limiter.return_value.acquire = Mock()

            result = fetch_for_unit(
                api_func=mock_api_func,
                kwargs={},
                page_size=10,
                max_retries=3,
                base_delay=1.0,
                supports_pagination=True,
                pagination_type="skip_take",
            )

        assert result == []

    def test_non_list_result_handling(self):
        """Test handling of non-list results."""
        mock_api_func = Mock(return_value="single_item")

        with patch("time.sleep"), patch(
            "src.evo_client.utils.pagination_utils.RateLimiter"
        ) as mock_rate_limiter:
            mock_rate_limiter.return_value.acquire = Mock()

            result = fetch_for_unit(
                api_func=mock_api_func,
                kwargs={},
                page_size=10,
                max_retries=3,
                base_delay=1.0,
                supports_pagination=True,
                pagination_type="skip_take",
            )

        assert result == ["single_item"]


class TestPaginatedApiCall:
    """Test suite for paginated_api_call function."""

    def test_successful_paginated_call(self):
        """Test successful paginated API call."""
        mock_api_func = Mock(return_value=["item1", "item2"])
        mock_api_func.__name__ = "test_api_func"

        with patch(
            "src.evo_client.utils.pagination_utils.fetch_for_unit"
        ) as mock_fetch:
            mock_fetch.return_value = ["item1", "item2", "item3"]

            result = paginated_api_call(
                api_func=mock_api_func,
                page_size=50,
                max_retries=5,
                param1="value1",
                param2="value2",
            )

        assert result == ["item1", "item2", "item3"]
        mock_fetch.assert_called_once()

    def test_invalid_pagination_type(self):
        """Test error handling for invalid pagination type."""
        mock_api_func = Mock()

        with pytest.raises(ValueError) as exc_info:
            paginated_api_call(api_func=mock_api_func, pagination_type="invalid_type")

        assert "Unsupported pagination_type" in str(exc_info.value)

    def test_anonymous_function_handling(self):
        """Test handling of functions without __name__ attribute."""
        mock_api_func = Mock(spec=["__call__"])  # Mock without __name__

        with patch(
            "src.evo_client.utils.pagination_utils.fetch_for_unit"
        ) as mock_fetch, patch("src.evo_client.utils.pagination_utils.logger"):
            mock_fetch.return_value = ["result"]

            result = paginated_api_call(api_func=mock_api_func)

        assert result == ["result"]

    def test_exception_handling_with_partial_results(self):
        """Test handling of exceptions with partial results returned."""
        mock_api_func = Mock()
        mock_api_func.__name__ = "test_func"

        with patch(
            "src.evo_client.utils.pagination_utils.fetch_for_unit"
        ) as mock_fetch, patch(
            "src.evo_client.utils.pagination_utils.logger"
        ) as mock_logger:
            mock_fetch.side_effect = Exception("API Error")

            result = paginated_api_call(api_func=mock_api_func)

        assert result == []  # Should return empty list on error
        mock_logger.error.assert_called()
        mock_logger.warning.assert_called()

    def test_all_parameters_passed_correctly(self):
        """Test that all parameters are passed correctly to fetch_for_unit."""
        mock_api_func = Mock()
        mock_api_func.__name__ = "test_func"

        with patch(
            "src.evo_client.utils.pagination_utils.fetch_for_unit"
        ) as mock_fetch:
            mock_fetch.return_value = []

            paginated_api_call(
                api_func=mock_api_func,
                page_size=25,
                max_retries=10,
                base_delay=2.0,
                supports_pagination=False,
                pagination_type="page_page_size",
                branch_id="test_branch",
                post_request_delay=0.5,
                custom_param="test_value",
            )

        mock_fetch.assert_called_once_with(
            branch_id="test_branch",
            api_func=mock_api_func,
            kwargs={"custom_param": "test_value"},
            page_size=25,
            max_retries=10,
            base_delay=2.0,
            supports_pagination=False,
            pagination_type="page_page_size",
            post_request_delay=0.5,
        )

    def test_non_list_result_from_fetch_for_unit(self):
        """Test handling when fetch_for_unit returns non-list result."""
        mock_api_func = Mock()
        mock_api_func.__name__ = "test_func"

        with patch(
            "src.evo_client.utils.pagination_utils.fetch_for_unit"
        ) as mock_fetch:
            mock_fetch.return_value = "single_result"

            result = paginated_api_call(api_func=mock_api_func)

        assert result == ["single_result"]
