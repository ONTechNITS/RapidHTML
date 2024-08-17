import abc


class Renderable(abc.ABC):
    """
    Base renderable class

    Defines anything that should be rendered when placed into a
    RapidHTMLResponse. Any class that inherits from this should define it's own
    `render` method. The ooutput of this method should be a string that can be
    used in a modern web browser.
    """

    @abc.abstractmethod
    def render(self) -> str: ...
