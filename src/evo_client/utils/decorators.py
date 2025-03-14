import functools
from typing import Any, Callable, TypeVar

from loguru import logger
from rich.console import Console
from rich.panel import Panel

from ..exceptions.api_exceptions import ApiException

console = Console()

T = TypeVar("T", bound=Callable[..., Any])


def handle_api_errors(func: T) -> T:
    """Decorator to handle API errors gracefully."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ApiException as e:
            logger.error(f"API error: {str(e)}")
            console.print(Panel(f"API error: {str(e)}", style="red"))
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            console.print(Panel(f"Unexpected error: {str(e)}", style="red"))

    return wrapper
