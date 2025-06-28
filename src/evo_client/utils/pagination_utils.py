"""Pagination utilities for API calls with improved typing and testability."""

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from threading import Lock as ThreadLock
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    ParamSpec,
    Protocol,
    TypeVar,
    Union,
)

from loguru import logger

from ..exceptions.api_exceptions import ApiException

P = ParamSpec("P")
T = TypeVar("T")


class RateLimiterProtocol(Protocol):
    """Protocol for rate limiter implementations."""

    def acquire(self) -> None:
        """Wait until a request can be made, respecting rate limits."""
        ...


@dataclass
class PaginationConfig:
    """Configuration for pagination behavior."""

    page_size: int = 50
    max_retries: int = 5
    base_delay: float = 1.5
    post_request_delay: float = 1.0
    pagination_type: str = "skip_take"
    supports_pagination: bool = True

    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.pagination_type not in ("skip_take", "page_page_size"):
            raise ValueError("pagination_type must be 'skip_take' or 'page_page_size'")
        if self.page_size <= 0:
            raise ValueError("page_size must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""

    max_retries: int = 5
    base_delay: float = 1.5
    exponential_backoff: bool = True

    def __post_init__(self):
        """Validate retry configuration."""
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.base_delay < 0:
            raise ValueError("base_delay must be non-negative")


@dataclass
class PaginationResult:
    """Result of a paginated API call operation."""

    data: List[Any]
    success: bool = True
    error_message: Optional[str] = None
    total_requests: int = 0
    total_retries: int = 0

    @property
    def has_errors(self) -> bool:
        """Check if the operation had errors."""
        return not self.success or self.error_message is not None


class RateLimiter:
    """Thread-safe rate limiter to ensure API limits are respected."""

    def __init__(self, max_requests: int = 40, time_window: int = 60):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum requests allowed in time window
            time_window: Time window in seconds
        """
        if max_requests <= 0:
            raise ValueError("max_requests must be positive")
        if time_window <= 0:
            raise ValueError("time_window must be positive")

        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: List[float] = []
        self._lock = ThreadLock()

    def acquire(self) -> None:
        """Wait until a request can be made, respecting rate limits."""
        with self._lock:
            now = time.time()
            # Remove old requests outside the time window
            self.requests = [t for t in self.requests if now - t < self.time_window]

            if len(self.requests) >= self.max_requests:
                # Calculate sleep time until we can make another request
                sleep_time = self.requests[0] + self.time_window - now
                if sleep_time > 0:
                    logger.warning(
                        f"Rate limit reached, waiting {sleep_time:.2f}s before next request"
                    )
                    time.sleep(sleep_time)
                    # Clean old requests again after sleeping
                    now = time.time()
                    self.requests = [
                        t for t in self.requests if now - t < self.time_window
                    ]

            self.requests.append(now)

    def reset(self) -> None:
        """Reset the rate limiter state (useful for testing)."""
        with self._lock:
            self.requests.clear()


class RetryHandler:
    """Handles retry logic with exponential backoff."""

    def __init__(self, config: RetryConfig):
        self.config = config

    def extract_retry_after(self, error_message: str) -> float:
        """
        Extract Retry-After value from error message.

        Args:
            error_message: Error message that might contain Retry-After header

        Returns:
            Retry delay in seconds, defaults to 1.0 if not found
        """
        retry_after = 1.0
        if "Retry-After:" in error_message:
            try:
                # Parse "Retry-After: <seconds>" format
                parts = error_message.split("Retry-After:")
                if len(parts) > 1:
                    after_part = parts[1].strip()
                    # Find first numeric value
                    for token in after_part.split():
                        if token.isdigit():
                            retry_after = float(token)
                            break
            except (IndexError, ValueError) as e:
                logger.debug(f"Failed to parse Retry-After header: {e}")
        return retry_after

    def compute_backoff_delay(self, attempt: int, exception: Exception) -> float:
        """
        Compute backoff delay based on attempt count and exception type.

        Args:
            attempt: Current attempt number (1-based)
            exception: Exception that triggered the retry

        Returns:
            Delay in seconds before next retry
        """
        if self.config.exponential_backoff:
            delay = self.config.base_delay * (2 ** (attempt - 1))
        else:
            delay = self.config.base_delay

        # Handle rate limiting (429 Too Many Requests)
        error_msg = str(exception)
        if "429" in error_msg or "Too Many Requests" in error_msg:
            retry_after = self.extract_retry_after(error_msg)
            delay = max(delay, retry_after)

        return delay


class ApiCallExecutor:
    """Executes API calls with retry logic and rate limiting."""

    def __init__(
        self,
        rate_limiter: Optional[RateLimiterProtocol] = None,
        retry_handler: Optional[RetryHandler] = None,
    ):
        self.rate_limiter = rate_limiter or RateLimiter()
        self.retry_handler = retry_handler or RetryHandler(RetryConfig())

    def execute_with_retry(
        self,
        api_func: Callable[P, T],
        context: str = "API call",
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        """
        Execute API call with retry logic.

        Args:
            api_func: Function to call
            context: Context description for logging
            *args: Arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            Result from the API function

        Raises:
            Exception: If max retries exceeded
        """
        for attempt in range(1, self.retry_handler.config.max_retries + 1):
            self.rate_limiter.acquire()

            try:
                result = api_func(*args, **kwargs)
                if attempt > 1:
                    logger.info(f"{context} succeeded on attempt {attempt}")
                return result

            except (ApiException, Exception) as e:
                logger.warning(
                    f"{context} failed on attempt {attempt}/{self.retry_handler.config.max_retries}: {e}"
                )

                if attempt == self.retry_handler.config.max_retries:
                    logger.error(f"Max retries reached for {context}")
                    raise

                delay = self.retry_handler.compute_backoff_delay(attempt, e)
                logger.info(f"Retrying {context} in {delay:.2f}s...")
                time.sleep(delay)

        # This should never be reached due to the raise above
        raise RuntimeError("Unexpected end of retry loop")


class PaginatedApiCaller:
    """Main class for handling paginated API calls."""

    def __init__(
        self,
        executor: Optional[ApiCallExecutor] = None,
        default_config: Optional[PaginationConfig] = None,
    ):
        self.executor = executor or ApiCallExecutor()
        self.default_config = default_config or PaginationConfig()

    def _build_pagination_params(
        self, page: int, config: PaginationConfig
    ) -> Dict[str, Any]:
        """Build pagination parameters based on pagination type."""
        if config.pagination_type == "skip_take":
            return {"take": config.page_size, "skip": page * config.page_size}
        else:  # "page_page_size"
            return {"page": page, "page_size": config.page_size}

    def fetch_all_pages(
        self,
        api_func: Callable[P, List[T]],
        config: Optional[PaginationConfig] = None,
        branch_id_logging: str = "unknown",
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> PaginationResult:
        """
        Fetch all pages of data from a paginated API.

        Args:
            api_func: API function to call
            config: Pagination configuration (uses default if None)
            branch_id: Identifier for logging context
            **api_kwargs: Additional arguments for the API function

        Returns:
            PaginationResult with data and metadata
        """
        config = config or self.default_config
        results: List[T] = []
        page = 0
        total_requests = 0
        total_retries = 0

        func_name = getattr(api_func, "__name__", "unknown_function")
        logger.debug(
            f"Starting paginated fetch for {func_name} (branch: {branch_id_logging})"
        )

        try:
            while True:
                # Build call arguments
                if config.supports_pagination:
                    pagination_params = self._build_pagination_params(page, config)
                    kwargs.update(pagination_params)

                context = f"{func_name} page {page} (branch: {branch_id_logging})"

                try:
                    # Execute API call with retry logic
                    page_result = self.executor.execute_with_retry(
                        api_func, context, *args, **kwargs
                    )
                    total_requests += 1

                    # Add delay after successful request
                    if config.post_request_delay > 0:
                        time.sleep(config.post_request_delay)

                except Exception as e:
                    total_retries += self.executor.retry_handler.config.max_retries
                    return PaginationResult(
                        data=results,
                        success=False,
                        error_message=str(e),
                        total_requests=total_requests,
                        total_retries=total_retries,
                    )

                # Process results
                if not page_result:
                    break

                if isinstance(page_result, list):
                    results.extend(page_result)
                    # Check if we got fewer results than requested (last page)
                    if (
                        len(page_result) < config.page_size
                        or not config.supports_pagination
                    ):
                        break
                else:
                    # Single result (non-list response)
                    results.append(page_result)
                    break

                page += 1

        except Exception as e:
            logger.error(f"Unexpected error in paginated fetch: {e}")
            return PaginationResult(
                data=results,
                success=False,
                error_message=str(e),
                total_requests=total_requests,
                total_retries=total_retries,
            )

        logger.debug(
            f"Completed paginated fetch for {func_name}: {len(results)} items, "
            f"{total_requests} requests, {total_retries} retries"
        )

        return PaginationResult(
            data=results,
            success=True,
            total_requests=total_requests,
            total_retries=total_retries,
        )


# Factory function for backward compatibility
def create_paginated_caller(
    max_requests_per_minute: int = 40, max_retries: int = 5, base_delay: float = 1.5
) -> PaginatedApiCaller:
    """
    Create a configured PaginatedApiCaller instance.

    Args:
        max_requests_per_minute: Rate limit for API calls
        max_retries: Maximum retry attempts
        base_delay: Base delay for exponential backoff

    Returns:
        Configured PaginatedApiCaller instance
    """
    rate_limiter = RateLimiter(max_requests=max_requests_per_minute, time_window=60)
    retry_handler = RetryHandler(
        RetryConfig(max_retries=max_retries, base_delay=base_delay)
    )
    executor = ApiCallExecutor(rate_limiter=rate_limiter, retry_handler=retry_handler)

    return PaginatedApiCaller(executor=executor)


# Backward compatibility function
def paginated_api_call(
    api_func: Callable[P, List[T]],
    page_size: int = 50,
    max_retries: int = 5,
    base_delay: float = 1.5,
    supports_pagination: bool = True,
    pagination_type: str = "skip_take",
    branch_id_logging: str = "NOT INFORMED",
    post_request_delay: float = 1.0,
    *args: P.args,
    **kwargs: P.kwargs,
) -> List[T]:
    """
    Execute paginated API calls with retry logic (backward compatibility).

    Args:
        api_func: The API function to call
        page_size: Number of items to request per page
        max_retries: Maximum number of retry attempts for failed calls
        base_delay: Base delay in seconds for retry backoff
        supports_pagination: Whether the API supports pagination
        pagination_type: Type of pagination ('skip_take' or 'page_page_size')
        branch_id: Identifier for the branch/unit being processed
        post_request_delay: Delay in seconds after each successful API call
        **kwargs: Additional arguments to pass to the API function

    Returns:
        List of results from all pages
    """
    config = PaginationConfig(
        page_size=page_size,
        max_retries=max_retries,
        base_delay=base_delay,
        supports_pagination=supports_pagination,
        pagination_type=pagination_type,
        post_request_delay=post_request_delay,
    )

    caller = create_paginated_caller(max_retries=max_retries, base_delay=base_delay)
    result = caller.fetch_all_pages(
        api_func,
        config,
        branch_id_logging=branch_id_logging,
        *args,
        **kwargs,
    )

    if not result.success and result.error_message:
        logger.warning(
            f"Returning partial results due to error: {result.error_message}"
        )

    return result.data
