import inspect
import pathlib

from functools import lru_cache

from starlette.applications import Starlette


@lru_cache
def get_app() -> "Starlette":
    """Returns the current Starlette application instance.

    Returns:
        Starlette: The current Starlette application instance.
    """
    # Get the current Starlette application instance
    # TODO: Find a better way to get the current Starlette application instance
    for frame in inspect.stack():
        for var in frame.frame.f_locals.values():
            if isinstance(var, Starlette):
                return var


@lru_cache
def get_default_favicon() -> bytes:
    """Get the default RapidHTML favicon.

    Returns:
        bytes: The default RapidHTML favicon.
    """
    path = pathlib.Path(__file__).parent.parent / "static" / "RapidHTML.svg"
    with open(path, "rb") as f:
        return f.read()
