from typing import Callable, TypeVar
from functools import wraps

from lsm_project.event_logger.event_logger import EventLogger


T = TypeVar("T")


def log_errors(event_loger: EventLogger) -> Callable:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:

        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                event_loger.error(f"{func.__name__} || {e}")
                raise e

        return wrapper

    return decorator
