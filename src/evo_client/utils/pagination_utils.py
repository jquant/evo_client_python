from typing import List, Any, Callable, Dict, TypeVar
from loguru import logger
import time
from threading import Lock as ThreadLock

from ..exceptions.api_exceptions import ApiException

T = TypeVar("T")


class RateLimiter:
    """Global rate limiter to ensure we don't exceed API limits."""

    def __init__(self, max_requests: int = 35, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: List[float] = []
        self._lock = ThreadLock()

    def acquire(self):
        """Wait until a request can be made, respecting rate limits."""
        with self._lock:
            now = time.time()
            # Remove old requests
            self.requests = [t for t in self.requests if now - t < self.time_window]

            if len(self.requests) >= self.max_requests:
                # Calculate sleep time until we can make another request
                sleep_time = self.requests[0] + self.time_window - now
                if sleep_time > 0:
                    logger.warning(
                        f"Rate limit reached, waiting {sleep_time:.2f}s before next request."
                    )
                    time.sleep(sleep_time)
                    # After sleeping, clean old requests again
                    now = time.time()
                    self.requests = [
                        t for t in self.requests if now - t < self.time_window
                    ]

            self.requests.append(now)


def extract_retry_after(error_message: str) -> float:
    """
    Attempt to extract a Retry-After value from an error message.
    Defaults to 1 second if not found.
    """
    retry_after = 1.0
    if "Retry-After:" in error_message:
        try:
            # Assuming the format "Retry-After: <seconds>"
            parts = error_message.split("Retry-After:")
            if len(parts) > 1:
                after_part = parts[1].strip()
                # Take the first integer we find
                for token in after_part.split():
                    if token.isdigit():
                        retry_after = float(token)
                        break
        except (IndexError, ValueError):
            pass
    return retry_after


def compute_backoff_delay(
    base_delay: float, attempt: int, exception: Exception
) -> float:
    """
    Compute a backoff delay based on the attempt count and presence of rate limit hints.
    Uses exponential backoff and checks for 429 'Too Many Requests' errors.
    """
    delay = base_delay * (2 ** (attempt - 1))
    msg = str(exception)
    if "429" in msg or "Too Many Requests" in msg:
        delay = max(delay, extract_retry_after(msg))
    return delay


def fetch_for_unit(
    unit_id: str,
    api_func: Callable[..., List[T]],
    kwargs: Dict,
    page_size: int,
    max_retries: int,
    base_delay: float,
    supports_pagination: bool,
    pagination_type: str,
) -> List[T]:
    """Fetch all pages of data for a single unit, handling pagination and retries."""
    # Create rate limiter inside the process
    rate_limiter = RateLimiter(max_requests=5, time_window=1)
    unit_results: List[T] = []
    page = 0

    while True:
        call_kwargs = {**kwargs, "async_req": False}
        if supports_pagination:
            if pagination_type == "skip_take":
                call_kwargs.update({"take": page_size, "skip": page * page_size})
            else:  # "page_page_size"
                call_kwargs.update({"page": page, "page_size": page_size})

        for attempt in range(1, max_retries + 1):
            rate_limiter.acquire()
            try:
                result = api_func(**call_kwargs)
                time.sleep(1)

                if not result:
                    return unit_results

                if isinstance(result, list):
                    unit_results.extend(result)
                    if len(result) < page_size or not supports_pagination:
                        return unit_results
                else:
                    unit_results.append(result)
                    if not supports_pagination:
                        return unit_results

                page += 1
                break

            except (ApiException, Exception) as e:
                logger.warning(
                    f"Exception for unit {unit_id}, page {page}, attempt {attempt}/{max_retries}: {e}"
                )
                if attempt == max_retries:
                    logger.error(
                        f"Max retries reached for unit {unit_id}, page {page}."
                    )
                    raise ValueError(
                        f"Max retries reached for unit {unit_id}, page {page}: {e}"
                    )
                delay = compute_backoff_delay(base_delay, attempt, e)
                logger.info(f"Retrying unit {unit_id}, page {page} in {delay:.2f}s...")
                time.sleep(delay)

    return unit_results


def paginated_api_call(
    api_func: Callable[..., List[T]],
    unit_id: str,
    page_size: int = 50,
    max_retries: int = 5,
    base_delay: float = 1.5,
    supports_pagination: bool = True,
    pagination_type: str = "skip_take",
    **kwargs,
) -> List[T]:
    """Execute paginated API calls with retry logic."""
    if pagination_type not in ("skip_take", "page_page_size"):
        raise ValueError(
            "Unsupported pagination_type. Use 'skip_take' or 'page_page_size'."
        )

    func_name = (
        api_func.__name__ if hasattr(api_func, "__name__") else "anonymous function"
    )
    logger.debug(
        f"Starting paginated API calls for {func_name} with unit_id {unit_id}."
    )

    flat_results: List[Any] = []
    try:
        result = fetch_for_unit(
            unit_id=unit_id,
            api_func=api_func,
            kwargs=kwargs,
            page_size=page_size,
            max_retries=max_retries,
            base_delay=base_delay,
            supports_pagination=supports_pagination,
            pagination_type=pagination_type,
        )
        if isinstance(result, list):
            flat_results.extend(result)
        else:
            flat_results.append(result)
    except Exception as e:
        logger.error(f"Error fetching for unit {unit_id}: {e}")

    return flat_results
