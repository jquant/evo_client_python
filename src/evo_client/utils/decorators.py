"""API error handling decorators."""

import functools
from typing import Callable, TypeVar, ParamSpec
from rich.console import Console
from rich.panel import Panel
from loguru import logger

from ..exceptions.api_exceptions import ApiException

P = ParamSpec("P")
T = TypeVar("T")

console = Console()


def handle_api_errors(func: Callable[P, T]) -> Callable[P, T | None]:
    """
    Decorator to handle API errors gracefully.

    Catches both API exceptions and generic exceptions, logs them,
    and displays user-friendly error messages using Rich panels.

    Args:
        func: The function to wrap

    Returns:
        The wrapped function that handles exceptions
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T | None:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, ApiException):
                error_msg = f"API error: {str(e)}"
                logger.error(error_msg)
            else:
                error_msg = f"Unexpected error: {str(e)}"
                logger.error(error_msg)

            error_panel = Panel(error_msg, title="❌ Error", border_style="red")
            console.print(error_panel)
            return None

    return wrapper
