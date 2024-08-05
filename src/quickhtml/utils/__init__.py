import typing
import inspect

from functools import lru_cache

if typing.TYPE_CHECKING:
    from quickhtml import QuickHTML

@lru_cache
def get_app() -> "QuickHTML":
    """Returns the current FastAPI application instance.

    Returns:
        QuickHTML: The current FastAPI application instance.
    """
    from quickhtml import QuickHTML

    # Get the current FastAPI application instance
    # TODO: Find a better way to get the current FastAPI application instance
    for frame in inspect.stack():
        for var in frame.frame.f_locals.values():
            if isinstance(var, QuickHTML):
                return var