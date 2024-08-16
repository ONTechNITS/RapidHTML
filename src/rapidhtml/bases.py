import abc


class Renderable:
    @abc.abstractmethod
    def render(self): ...
