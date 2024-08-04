from __future__ import annotations

import typing
import inspect

from collections.abc import Iterable

if typing.TYPE_CHECKING:
    from quickhtml import QuickHTML


class BaseTag:
    """
    Represents a base HTML tag.

    Args:
        *tags: Variable length arguments representing child tags.
        **attrs: Keyword arguments representing tag attributes.

    Attributes:
        tag (str): The name of the HTML tag.
        tags (list): A list of child tags.
        attrs (dict): A dictionary of tag attributes.

    Methods:
        add_head(head): Adds a head tag to the beginning of the list of child tags.
        render(): Renders the HTML representation of the tag and its child tags.
    """

    def __init__(self, *tags, callback: typing.Callable = None, **attrs):
        self.tag = self.__class__.__qualname__.lower()
        self.tags = list(tags)
        self.attrs = attrs
        if callback:
            self.add_callback(callback)

    @property
    def app(self) -> "QuickHTML":
        """
        Returns the current FastAPI application instance.

        Returns:
            FastAPI: The current FastAPI application instance.
        """
        from quickhtml import QuickHTML

        # Get the current FastAPI application instance
        # TODO: Find a better way to get the current FastAPI application instance
        for var in inspect.stack()[-1].frame.f_locals.values():
            if isinstance(var, QuickHTML):
                app = var
                break

        return app

    def add_callback(self, callback: typing.Callable):
        """
        Adds a callback function to the tag.

        Args:
            callback (typing.Callable): The callback function to be added.
        """
        self.app.add_route(
            f"/python-callbacks/{id(callback)}",
            callback,
        )

        self.attrs["hx-get"] = self.callback_route

    def add_head(self, head: typing.Iterable["BaseTag"] | "BaseTag"):
        """
        Adds a head tag to the beginning of the list of child tags.

        Args:
            head: The head tag to be added.
        """
        if not isinstance(head, Iterable):
            head = (head,)
        if head:
            self.tags.insert(0, Head(*head))

    def render(self):
        """
        Renders the HTML representation of the tag and its child tags.

        Returns:
            str: The HTML representation of the tag and its child tags.
        """
        # Apply tag attributes
        if self.attrs:
            ret_html = f"<{self.tag} "
            for key, value in self.attrs.items():
                # Translate the keyword argument class_ to class
                if key == "class_":
                    key = "class"

                # Translate value None to 'none'
                if value is None:
                    value = "none"

                # Replace underscores with hyphens
                key = key.replace("_", "-")
                ret_html += f"{key}='{value}' "
            else:
                ret_html = ret_html[:-1] + ">"
        else:
            ret_html = f"<{self.tag}>"

        # Recursively render child tags
        for tag in self.tags:
            if isinstance(tag, BaseTag):
                ret_html += tag.render()
            else:
                ret_html += tag

        # Close the tag
        ret_html += f"</{self.tag}>"
        return ret_html


class A(BaseTag): ...


class Abbr(BaseTag): ...


class Address(BaseTag): ...


class Area(BaseTag): ...


class Article(BaseTag): ...


class Aside(BaseTag): ...


class Audio(BaseTag): ...


class B(BaseTag): ...


class Base(BaseTag): ...


class Bdi(BaseTag): ...


class Bdo(BaseTag): ...


class Blockquote(BaseTag): ...


class Body(BaseTag): ...


class Br(BaseTag): ...


class Button(BaseTag): ...


class Canvas(BaseTag): ...


class Caption(BaseTag): ...


class Cite(BaseTag): ...


class Code(BaseTag): ...


class Col(BaseTag): ...


class Colgroup(BaseTag): ...


class Data(BaseTag): ...


class Datalist(BaseTag): ...


class Dd(BaseTag): ...


class Del(BaseTag): ...


class Details(BaseTag): ...


class Dfn(BaseTag): ...


class Dialog(BaseTag): ...


class Div(BaseTag): ...


class Dl(BaseTag): ...


class Dt(BaseTag): ...


class Em(BaseTag): ...


class Embed(BaseTag): ...


class Fencedframe(BaseTag): ...


class Fieldset(BaseTag): ...


class Figcaption(BaseTag): ...


class Figure(BaseTag): ...


class Footer(BaseTag): ...


class Form(BaseTag): ...


class H1(BaseTag): ...


class Head(BaseTag): ...


class Header(BaseTag): ...


class Hgroup(BaseTag): ...


class Hr(BaseTag): ...


class Html(BaseTag): ...


class I(BaseTag): ...


class Iframe(BaseTag): ...


class Img(BaseTag): ...


class Input(BaseTag): ...


class Ins(BaseTag): ...


class Kbd(BaseTag): ...


class Label(BaseTag): ...


class Legend(BaseTag): ...


class Li(BaseTag): ...


class Link(BaseTag): ...


class Main(BaseTag): ...


class Map(BaseTag): ...


class Mark(BaseTag): ...


class Menu(BaseTag): ...


class Meta(BaseTag): ...


class Meter(BaseTag): ...


class Nav(BaseTag): ...


class Noscript(BaseTag): ...


class Object(BaseTag): ...


class Ol(BaseTag): ...


class Optgroup(BaseTag): ...


class Option(BaseTag): ...


class Output(BaseTag): ...


class P(BaseTag): ...


class Picture(BaseTag): ...


class PortalExperimental(BaseTag): ...


class Pre(BaseTag): ...


class Progress(BaseTag): ...


class Q(BaseTag): ...


class Rp(BaseTag): ...


class Rt(BaseTag): ...


class Ruby(BaseTag): ...


class S(BaseTag): ...


class Samp(BaseTag): ...


class Script(BaseTag): ...


class Search(BaseTag): ...


class Section(BaseTag): ...


class Select(BaseTag): ...


class Slot(BaseTag): ...


class Small(BaseTag): ...


class Source(BaseTag): ...


class Span(BaseTag): ...


class Strong(BaseTag): ...


class Style(BaseTag): ...


class Sub(BaseTag): ...


class Summary(BaseTag): ...


class Sup(BaseTag): ...


class Table(BaseTag): ...


class Tbody(BaseTag): ...


class Td(BaseTag): ...


class Template(BaseTag): ...


class Textarea(BaseTag): ...


class Tfoot(BaseTag): ...


class Th(BaseTag): ...


class Thead(BaseTag): ...


class Time(BaseTag): ...


class Title(BaseTag): ...


class Tr(BaseTag): ...


class Track(BaseTag): ...


class U(BaseTag): ...


class Ul(BaseTag): ...


class Var(BaseTag): ...


class Video(BaseTag): ...


class Wbr(BaseTag): ...
