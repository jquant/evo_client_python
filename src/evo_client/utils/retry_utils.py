import time
from functools import wraps
from typing import Any, Callable, TypeVar

from loguru import logger

from ..exceptions.api_exceptions import ApiException

T = TypeVar('T')


def with_retry(
    max_retries: int = 3,
    base_delay: float = 1.5,
    error_message: str = "Operation failed"
) -> Callable:
    """
    Decorator for retrying operations with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay between retries (will be multiplied by 2^attempt)
        error_message: Message to log on failure
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                    return result
                    
                except Exception as e:
                    last_exception = e
                    
                    if "429" in str(e):  # Rate limit error
                        if attempt < max_retries - 1:
                            delay = base_delay * (2 ** attempt)
                            logger.warning(f"Rate limit hit, waiting {delay}s before retry {attempt + 1}/{max_retries}")
                            time.sleep(delay)
                            continue
                    elif "404" in str(e):
                        logger.warning(f"Endpoint not found: {str(e)}")
                        raise ApiException(f"Endpoint not found: {str(e)}")
                    
                    if attempt == max_retries - 1:
                        logger.error(f"{error_message}: {str(e)}")
                        raise ApiException(f"{error_message}: {str(e)}")
                    
                    # Add delay between retries
                    time.sleep(base_delay)
            
            # If we get here, all retries failed
            raise last_exception or ApiException(f"{error_message}: Unknown error")
            
        return wrapper
    return decorator


def retry_operation(
    operation: Callable[..., T],
    max_retries: int = 3,
    base_delay: float = 1.5,
    error_message: str = "Operation failed",
    **kwargs: Any
) -> T:
    """
    Retry an operation with exponential backoff.
    
    Args:
        operation: Function to retry
        max_retries: Maximum number of retry attempts
        base_delay: Base delay between retries (will be multiplied by 2^attempt)
        error_message: Message to log on failure
        **kwargs: Arguments to pass to the operation
        
    Returns:
        Operation result
        
    Raises:
        ApiException: If all retries fail
    """
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            result = operation(**kwargs)
            return result
            
        except Exception as e:
            last_exception = e
            
            if "429" in str(e):  # Rate limit error
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Rate limit hit, waiting {delay}s before retry {attempt + 1}/{max_retries}")
                    time.sleep(delay)
                    continue
            elif "404" in str(e):
                logger.warning(f"Endpoint not found: {str(e)}")
                raise ApiException(f"Endpoint not found: {str(e)}")
            
            if attempt == max_retries - 1:
                logger.error(f"{error_message}: {str(e)}")
                raise ApiException(f"{error_message}: {str(e)}")
            
            # Add delay between retries
            time.sleep(base_delay)
    
    # If we get here, all retries failed
    raise last_exception or ApiException(f"{error_message}: Unknown error") 