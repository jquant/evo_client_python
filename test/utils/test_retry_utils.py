"""Tests for retry_utils module."""

from unittest.mock import patch

import pytest

from src.evo_client.exceptions.api_exceptions import ApiException
from src.evo_client.utils.retry_utils import retry_operation, with_retry


class TestWithRetryDecorator:
    """Test suite for with_retry decorator."""

    def test_successful_function_no_retry_needed(self):
        """Test that successful function executes without retries."""

        @with_retry(max_retries=3)
        def successful_function(x, y):
            return x + y

        result = successful_function(2, 3)
        assert result == 5

    def test_function_succeeds_after_retries(self):
        """Test that function succeeds after some failed attempts."""
        call_count = 0

        @with_retry(max_retries=3, base_delay=0.01)  # Very short delay for testing
        def flaky_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("Temporary failure")
            return "success"

        with patch("time.sleep"):  # Mock sleep to speed up test
            result = flaky_function()

        assert result == "success"
        assert call_count == 3

    def test_max_retries_exceeded(self):
        """Test that function raises exception when max retries exceeded."""

        @with_retry(max_retries=2, base_delay=0.01)
        def always_failing_function():
            raise Exception("Always fails")

        with patch("time.sleep"), patch(
            "src.evo_client.utils.retry_utils.logger"
        ) as mock_logger:
            with pytest.raises(ApiException) as exc_info:
                always_failing_function()

            assert "Operation failed: Always fails" in str(exc_info.value)
            mock_logger.error.assert_called()

    def test_rate_limit_handling(self):
        """Test special handling for rate limit errors (429)."""
        call_count = 0

        @with_retry(max_retries=3, base_delay=0.01)
        def rate_limited_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("HTTP 429: Rate limit exceeded")
            return "success"

        with patch("time.sleep") as mock_sleep, patch(
            "src.evo_client.utils.retry_utils.logger"
        ) as mock_logger:
            result = rate_limited_function()

        assert result == "success"
        assert call_count == 3

        # Should have exponential backoff for rate limits
        assert mock_sleep.call_count >= 1
        mock_logger.warning.assert_called()

    def test_404_error_immediate_failure(self):
        """Test that 404 errors cause immediate failure without retries."""

        @with_retry(max_retries=3)
        def not_found_function():
            raise Exception("HTTP 404: Not found")

        with patch("src.evo_client.utils.retry_utils.logger") as mock_logger:
            with pytest.raises(ApiException) as exc_info:
                not_found_function()

            assert "Endpoint not found" in str(exc_info.value)
            mock_logger.warning.assert_called_with(
                "Endpoint not found: HTTP 404: Not found"
            )

    def test_custom_error_message(self):
        """Test that custom error messages are used."""

        @with_retry(max_retries=1, error_message="Custom operation failed")
        def failing_function():
            raise Exception("Test error")

        with patch("time.sleep"), patch(
            "src.evo_client.utils.retry_utils.logger"
        ) as mock_logger:
            with pytest.raises(ApiException) as exc_info:
                failing_function()

            assert "Custom operation failed: Test error" in str(exc_info.value)

    def test_exponential_backoff_rate_limits(self):
        """Test that exponential backoff is applied for rate limits."""

        @with_retry(max_retries=3, base_delay=0.1)
        def rate_limited_function():
            raise Exception("HTTP 429: Rate limit")

        with patch("time.sleep") as mock_sleep, patch(
            "src.evo_client.utils.retry_utils.logger"
        ):
            with pytest.raises(ApiException):
                rate_limited_function()

            # Should have called sleep with exponential backoff
            sleep_calls = [call[0][0] for call in mock_sleep.call_args_list]
            assert len(sleep_calls) >= 2
            # First sleep should be base_delay * 2^0 = 0.1
            # Second sleep should be base_delay * 2^1 = 0.2
            assert sleep_calls[0] == 0.1
            assert sleep_calls[1] == 0.2

    def test_function_with_args_and_kwargs(self):
        """Test that decorator preserves function arguments."""

        @with_retry(max_retries=1)
        def function_with_args(a, b, c=None, d=None):
            return f"a={a}, b={b}, c={c}, d={d}"

        result = function_with_args(1, 2, c=3, d=4)
        assert result == "a=1, b=2, c=3, d=4"

    def test_function_metadata_preservation(self):
        """Test that decorator preserves function metadata."""

        @with_retry()
        def original_function():
            """Original function docstring."""

        assert original_function.__name__ == "original_function"
        assert original_function.__doc__ == "Original function docstring."


class TestRetryOperation:
    """Test suite for retry_operation function."""

    def test_successful_operation_no_retry(self):
        """Test that successful operation executes without retries."""

        def successful_op(x, y):
            return x * y

        result = retry_operation(successful_op, x=3, y=4)
        assert result == 12

    def test_operation_succeeds_after_retries(self):
        """Test that operation succeeds after some failed attempts."""
        call_count = 0

        def flaky_operation(value):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("Temporary failure")
            return value * 2

        with patch("time.sleep"):
            result = retry_operation(
                flaky_operation, max_retries=3, base_delay=0.01, value=5
            )

        assert result == 10
        assert call_count == 3

    def test_max_retries_exceeded_operation(self):
        """Test that operation raises exception when max retries exceeded."""

        def always_failing_operation():
            raise Exception("Always fails")

        with patch("time.sleep"), patch(
            "src.evo_client.utils.retry_utils.logger"
        ) as mock_logger:
            with pytest.raises(ApiException) as exc_info:
                retry_operation(
                    always_failing_operation,
                    max_retries=2,
                    error_message="Custom operation failed",
                )

            assert "Custom operation failed: Always fails" in str(exc_info.value)
            mock_logger.error.assert_called()

    def test_rate_limit_handling_operation(self):
        """Test special handling for rate limit errors in retry_operation."""
        call_count = 0

        def rate_limited_operation():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception("HTTP 429: Rate limit exceeded")
            return "success"

        with patch("time.sleep") as mock_sleep, patch(
            "src.evo_client.utils.retry_utils.logger"
        ) as mock_logger:
            result = retry_operation(
                rate_limited_operation, max_retries=3, base_delay=0.01
            )

        assert result == "success"
        assert call_count == 3
        mock_logger.warning.assert_called()

    def test_404_error_immediate_failure_operation(self):
        """Test that 404 errors cause immediate failure in retry_operation."""

        def not_found_operation():
            raise Exception("HTTP 404: Not found")

        with patch("src.evo_client.utils.retry_utils.logger") as mock_logger:
            with pytest.raises(ApiException) as exc_info:
                retry_operation(not_found_operation)

            assert "Endpoint not found" in str(exc_info.value)
            mock_logger.warning.assert_called()

    def test_operation_with_no_exception_but_none_result(self):
        """Test edge case where operation returns None without exception."""

        def none_returning_operation():
            return None

        result = retry_operation(none_returning_operation)
        assert result is None

    def test_operation_kwargs_passing(self):
        """Test that kwargs are properly passed to the operation."""

        def operation_with_kwargs(a, b, c=None, d=None):
            return {"a": a, "b": b, "c": c, "d": d}

        result = retry_operation(operation_with_kwargs, a=1, b=2, c=3, d=4)

        assert result == {"a": 1, "b": 2, "c": 3, "d": 4}

    def test_unknown_error_fallback(self):
        """Test fallback behavior when no exception is captured but retries fail."""

        def mysterious_operation():
            # This simulates the edge case where last_exception might be None
            raise Exception("Mystery error")

        with patch("time.sleep"), patch("src.evo_client.utils.retry_utils.logger"):
            with pytest.raises(ApiException) as exc_info:
                retry_operation(mysterious_operation, max_retries=1)

            # Should still raise an exception
            assert "Operation failed" in str(exc_info.value)
