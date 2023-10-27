from typing import Callable, TypeVar
from functools import wraps

from lsm_project.event_logger.event_logger import EventLogger


event_logger = EventLogger()
T = TypeVar("T")


def log_errors(func: Callable[..., T]) -> Callable[..., T]:
    global event_logger

    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            event_logger.error(f"[{func.__name__}] {e}")
            raise e

    return wrapper
