# src/qtrader/providers/massive/utils.py

import time
import logging
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger(__name__)


def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Retry decorator for functions that may fail intermittently.
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logger.warning(
                        "Attempt %d/%d failed for %s: %s",
                        attempts,
                        max_attempts,
                        func.__name__,
                        e,
                    )
                    if attempts < max_attempts:
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error("All %d attempts failed for %s", max_attempts, func.__name__)
                        raise
        return wrapper

    return decorator
