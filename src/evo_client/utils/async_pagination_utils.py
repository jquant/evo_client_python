"""Async pagination utilities for API calls with improved typing and testability."""

import asyncio
import time
from abc import ABC, abstractmethod
from threading import Lock as ThreadLock
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Protocol,
    TypeVar,
    Union,
    Tuple,
    ParamSpec,
)

from loguru import logger

from ..exceptions.api_exceptions import ApiException
from .pagination_utils import PaginationConfig, RetryConfig, PaginationResult

T = TypeVar("T")
P = ParamSpec("P")


class AsyncRateLimiterProtocol(Protocol):
    """Protocol for async rate limiter implementations."""

    async def acquire(self) -> None:
        """Wait until a request can be made, respecting rate limits."""
        ...


class AsyncRateLimiter:
    """Thread-safe async rate limiter to ensure API limits are respected."""

    def __init__(self, max_requests: int = 40, time_window: int = 60):
        """
        Initialize async rate limiter.

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
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Wait until a request can be made, respecting rate limits."""
        async with self._lock:
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
                    await asyncio.sleep(sleep_time)
                    # Clean old requests again after sleeping
                    now = time.time()
                    self.requests = [
                        t for t in self.requests if now - t < self.time_window
                    ]

            self.requests.append(now)

    async def reset(self) -> None:
        """Reset the rate limiter state (useful for testing)."""
        async with self._lock:
            self.requests.clear()


class AsyncRetryHandler:
    """Handles async retry logic with exponential backoff."""

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


class AsyncApiCallExecutor:
    """Executes async API calls with retry logic and rate limiting."""

    def __init__(
        self,
        rate_limiter: Optional[AsyncRateLimiterProtocol] = None,
        retry_handler: Optional[AsyncRetryHandler] = None,
    ):
        self.rate_limiter = rate_limiter or AsyncRateLimiter()
        self.retry_handler = retry_handler or AsyncRetryHandler(RetryConfig())

    async def execute_with_retry(
        self,
        api_func: Callable[P, Awaitable[T]],
        context: str = "API call",
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        """
        Execute async API call with retry logic.

        Args:
            api_func: Async function to call
            context: Context description for logging
            *args: Arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            Result from the API function

        Raises:
            Exception: If max retries exceeded
        """
        for attempt in range(1, self.retry_handler.config.max_retries + 1):
            await self.rate_limiter.acquire()

            try:
                result = await api_func(*args, **kwargs)
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
                await asyncio.sleep(delay)

        # This should never be reached due to the raise above
        raise RuntimeError("Unexpected end of retry loop")


class AsyncPaginatedApiCaller:
    """Main class for handling async paginated API calls."""

    def __init__(
        self,
        executor: Optional[AsyncApiCallExecutor] = None,
        default_config: Optional[PaginationConfig] = None,
    ):
        self.executor = executor or AsyncApiCallExecutor()
        self.default_config = default_config or PaginationConfig()

    def _build_pagination_params(
        self, page: int, config: PaginationConfig
    ) -> Dict[str, Any]:
        """Build pagination parameters based on pagination type."""
        if config.pagination_type == "skip_take":
            return {"take": config.page_size, "skip": page * config.page_size}
        else:  # "page_page_size"
            return {"page": page, "page_size": config.page_size}

    async def fetch_all_pages(
        self,
        api_func: Callable[P, Awaitable[List[T]]],
        config: Optional[PaginationConfig] = None,
        branch_id_logging: str = "unknown",
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> PaginationResult:
        """
        Fetch all pages of data from a paginated API.

        Args:
            api_func: Async API function to call
            config: Pagination configuration (uses default if None)
            *args: Additional arguments for the API function
            **kwargs: Additional keyword arguments for the API function (including branch_id)

        Returns:
            PaginationResult with data and metadata
        """
        config = config or self.default_config
        results: List[T] = []
        page = 0
        total_requests = 0
        total_retries = 0

        # Extract branch_id for logging, default to "unknown"
        func_name = getattr(api_func, "__name__", "unknown_function")
        logger.debug(
            f"Starting async paginated fetch for {func_name} (branch: {branch_id_logging})"
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
                    page_result = await self.executor.execute_with_retry(
                        api_func, context, *args, **kwargs
                    )
                    total_requests += 1

                    # Add delay after successful request
                    if config.post_request_delay > 0:
                        await asyncio.sleep(config.post_request_delay)

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
            logger.error(f"Unexpected error in async paginated fetch: {e}")
            return PaginationResult(
                data=results,
                success=False,
                error_message=str(e),
                total_requests=total_requests,
                total_retries=total_retries,
            )

        logger.debug(
            f"Completed async paginated fetch for {func_name}: {len(results)} items, "
            f"{total_requests} requests, {total_retries} retries"
        )

        return PaginationResult(
            data=results,
            success=True,
            total_requests=total_requests,
            total_retries=total_retries,
        )

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        # Cleanup if needed
        pass


# Factory function for async pagination
def create_async_paginated_caller(
    max_requests_per_minute: int = 40, max_retries: int = 5, base_delay: float = 1.5
) -> AsyncPaginatedApiCaller:
    """
    Create a configured AsyncPaginatedApiCaller instance.

    Args:
        max_requests_per_minute: Rate limit for API calls
        max_retries: Maximum retry attempts
        base_delay: Base delay for exponential backoff

    Returns:
        Configured AsyncPaginatedApiCaller instance
    """
    rate_limiter = AsyncRateLimiter(
        max_requests=max_requests_per_minute, time_window=60
    )
    retry_handler = AsyncRetryHandler(
        RetryConfig(max_retries=max_retries, base_delay=base_delay)
    )
    executor = AsyncApiCallExecutor(
        rate_limiter=rate_limiter, retry_handler=retry_handler
    )

    return AsyncPaginatedApiCaller(executor=executor)


# Utility class for managing concurrent pagination
class ConcurrentPaginationManager:
    """Manages multiple concurrent pagination operations with proper resource limits."""

    def __init__(
        self,
        max_concurrent_operations: int = 5,
        global_rate_limiter: Optional[AsyncRateLimiterProtocol] = None,
    ):
        self.semaphore = asyncio.Semaphore(max_concurrent_operations)
        self.global_rate_limiter = global_rate_limiter or AsyncRateLimiter()

    async def fetch_multiple_branches(
        self,
        api_func: Callable[..., Awaitable[List[T]]],
        branch_configs: List[Dict[str, Any]],
        config: Optional[PaginationConfig] = None,
    ) -> Dict[str, PaginationResult]:
        """
        Fetch data for multiple branches concurrently.

        Args:
            api_func: Async API function to call
            branch_configs: List of configs, each with branch_id and optional kwargs
            config: Pagination configuration

        Returns:
            Dictionary mapping branch_id to PaginationResult
        """

        async def fetch_for_branch(
            branch_config: Dict[str, Any],
        ) -> Tuple[str, PaginationResult]:
            async with self.semaphore:
                branch_id = branch_config.get("branch_id", "unknown")

                # Create caller with shared rate limiter
                executor = AsyncApiCallExecutor(rate_limiter=self.global_rate_limiter)
                caller = AsyncPaginatedApiCaller(
                    executor=executor, default_config=config
                )

                # Pass the config to API function, branch_id goes to fetch_all_pages for logging
                api_kwargs = {
                    k: v for k, v in branch_config.items() if k != "branch_id"
                }
                api_kwargs["branch_id"] = branch_id  # Ensure branch_id is in API kwargs
                result = await caller.fetch_all_pages(
                    api_func,
                    config,
                    **api_kwargs,
                )
                return branch_id, result

        # Execute all branch fetches concurrently
        tasks = [fetch_for_branch(branch_config) for branch_config in branch_configs]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        branch_results = {}
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Branch fetch failed: {result}")
                continue

            # Explicitly check that result is a tuple before unpacking
            if isinstance(result, tuple) and len(result) == 2:
                branch_id, pagination_result = result
                branch_results[branch_id] = pagination_result
            else:
                logger.error(f"Unexpected result format: {result}")

        return branch_results


# Backward compatibility function
async def async_paginated_api_call(
    api_func: Callable[P, Awaitable[List[T]]],
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
    Execute async paginated API calls with retry logic (backward compatibility).

    Args:
        api_func: The async API function to call
        page_size: Number of items to request per page
        max_retries: Maximum number of retry attempts for failed calls
        base_delay: Base delay in seconds for retry backoff
        supports_pagination: Whether the API supports pagination
        pagination_type: Type of pagination ('skip_take' or 'page_page_size')
        branch_id: Identifier for the branch/unit being processed
        post_request_delay: Delay in seconds after each successful API call
        *args: Additional arguments for the API function
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

    caller = create_async_paginated_caller(
        max_retries=max_retries, base_delay=base_delay
    )
    result = await caller.fetch_all_pages(
        api_func, config, branch_id_logging=branch_id_logging, *args, **kwargs
    )

    if not result.success and result.error_message:
        logger.warning(
            f"Returning partial results due to error: {result.error_message}"
        )

    return result.data
