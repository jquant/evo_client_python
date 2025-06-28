"""Tests for decorators module."""

import pytest
from unittest.mock import Mock, patch
from rich.console import Console

from src.evo_client.utils.decorators import handle_api_errors
from src.evo_client.exceptions.api_exceptions import ApiException


class TestHandleApiErrors:
    """Test suite for handle_api_errors decorator."""

    def test_successful_function_execution(self):
        """Test that decorator doesn't interfere with successful function execution."""

        @handle_api_errors
        def successful_function(x, y):
            return x + y

        result = successful_function(2, 3)
        assert result == 5

    def test_api_exception_handling(self):
        """Test that API exceptions are caught and logged properly."""

        @handle_api_errors
        def function_with_api_error():
            raise ApiException("Test API error")

        with patch("src.evo_client.utils.decorators.logger") as mock_logger, patch(
            "src.evo_client.utils.decorators.console"
        ) as mock_console:

            result = function_with_api_error()

            # Should return None (no return statement in wrapper)
            assert result is None

            # Should log the error
            mock_logger.error.assert_called_once_with("API error: Test API error")

            # Should print error panel - check that console.print was called
            mock_console.print.assert_called_once()

            # Verify the panel contains the expected error message
            panel_call_args = mock_console.print.call_args[0][0]
            assert hasattr(
                panel_call_args, "renderable"
            )  # Panel has renderable attribute
            assert "API error: Test API error" in panel_call_args.renderable

    def test_generic_exception_handling(self):
        """Test that generic exceptions are caught and logged properly."""

        @handle_api_errors
        def function_with_generic_error():
            raise ValueError("Test generic error")

        with patch("src.evo_client.utils.decorators.logger") as mock_logger, patch(
            "src.evo_client.utils.decorators.console"
        ) as mock_console:

            result = function_with_generic_error()

            # Should return None
            assert result is None

            # Should log the unexpected error
            mock_logger.error.assert_called_once_with(
                "Unexpected error: Test generic error"
            )

            # Should print error panel - check that console.print was called
            mock_console.print.assert_called_once()

            # Verify the panel contains the expected error message
            panel_call_args = mock_console.print.call_args[0][0]
            assert hasattr(
                panel_call_args, "renderable"
            )  # Panel has renderable attribute
            assert "Unexpected error: Test generic error" in panel_call_args.renderable

    def test_function_with_args_and_kwargs(self):
        """Test that decorator preserves function arguments."""

        @handle_api_errors
        def function_with_args(a, b, c=None, d=None):
            return f"a={a}, b={b}, c={c}, d={d}"

        result = function_with_args(1, 2, c=3, d=4)
        assert result == "a=1, b=2, c=3, d=4"

    def test_function_metadata_preservation(self):
        """Test that decorator preserves function metadata."""

        @handle_api_errors
        def original_function():
            """Original function docstring."""
            pass

        assert original_function.__name__ == "original_function"
        assert original_function.__doc__ == "Original function docstring."

    def test_multiple_decorators_compatibility(self):
        """Test that handle_api_errors works with other decorators."""

        def another_decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if result is not None:
                    return f"decorated: {result}"
                return result

            return wrapper

        @another_decorator
        @handle_api_errors
        def decorated_function(x):
            return x * 2

        result = decorated_function(5)
        assert result == "decorated: 10"

    def test_exception_in_function_with_return_value(self):
        """Test behavior when decorated function normally returns a value but raises exception."""

        @handle_api_errors
        def function_that_should_return():
            if True:  # Simulate condition that causes error
                raise ApiException("Error occurred")
            return "success"

        with patch("src.evo_client.utils.decorators.logger"), patch(
            "src.evo_client.utils.decorators.console"
        ):

            result = function_that_should_return()
            assert result is None  # Should return None on exception
