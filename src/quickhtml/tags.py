from __future__ import annotations

import html
import typing

from collections.abc import Iterable

from quickhtml.utils import get_app

if typing.TYPE_CHECKING:
    from quickhtml import QuickHTML
    from starlette.applications import Starlette


class BaseTag:
    """
    Represents a base HTML tag.

    Args:
        *tags: Variable length arguments representing child tags.
        callback (typing.Callable): A callback function to be added to the tag.
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

        if self.tags and self.__self_closing:
            raise ValueError(
                f"{self.tag} does not support nesting other tags within it"
            )

        self.__closing_tag = f"</{self.tag}>" if not self.__self_closing else "/>"

    def __init_subclass__(cls, self_closing: bool = False, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.__self_closing = self_closing

    @property
    def app(self) -> "QuickHTML" | "Starlette":
        """
        Returns the current QuickHTML application instance.

        Returns:
            QuickHTML | Starlette: The current QuickHTML application instance.
        """
        return get_app()

    def add_callback(self, callback: typing.Callable):
        """
        Adds a callback function to the tag.

        Args:
            callback (typing.Callable): The callback function to be added.
        """
        self.callback_route = f"/python-callbacks/{id(callback)}"

        self.app.add_route(
            self.callback_route,
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

        ret_html = f"<{self.tag} "

        for key, value in self.attrs.items():
            key = key.rstrip("_")

            # Translate value None to 'none'
            if value is None:
                value = "none"

            # Replace underscores with hyphens
            key = key.replace("_", "-")
            ret_html += f"{key}='{value}' "

        if not self.__self_closing:
            ret_html += ">"

        # Recursively render child tags
        for tag in self.tags:
            if isinstance(tag, BaseTag):
                ret_html += tag.render()
            elif hasattr(tag, "__str__"):
                ret_html += html.escape(str(tag))
            else:
                raise TypeError(f"Unexpected tag type {type(tag)}. {tag}")

        # Close the tag
        ret_html += self.__closing_tag

        return ret_html


class A(BaseTag): ...


class Abbr(BaseTag): ...


class Address(BaseTag): ...


class Area(BaseTag, self_closing=True): ...


class Article(BaseTag): ...


class Aside(BaseTag): ...


class Audio(BaseTag): ...


class B(BaseTag): ...


class Base(BaseTag, self_closing=True): ...


class Bdi(BaseTag): ...


class Bdo(BaseTag): ...


class Blockquote(BaseTag): ...


class Body(BaseTag): ...


class Br(BaseTag, self_closing=True): ...


class Button(BaseTag): ...


class Canvas(BaseTag): ...


class Caption(BaseTag): ...


class Cite(BaseTag): ...


class Code(BaseTag): ...


class Col(BaseTag, self_closing=True): ...


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


class Embed(BaseTag, self_closing=True): ...


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


class Hr(BaseTag, self_closing=True): ...


class Html(BaseTag): ...


class I(BaseTag): ...


class Iframe(BaseTag): ...


class Img(BaseTag, self_closing=True): ...


class Input(BaseTag, self_closing=True): ...


class Ins(BaseTag): ...


class Kbd(BaseTag): ...


class Label(BaseTag): ...


class Legend(BaseTag): ...


class Li(BaseTag): ...


class Link(BaseTag, self_closing=True): ...


class Main(BaseTag): ...


class Map(BaseTag): ...


class Mark(BaseTag): ...


class Menu(BaseTag): ...


class Meta(BaseTag, self_closing=True): ...


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


class Source(BaseTag, self_closing=True): ...


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


class Track(BaseTag, self_closing=True): ...


class U(BaseTag): ...


class Ul(BaseTag): ...


class Var(BaseTag): ...


class Video(BaseTag): ...


class Wbr(BaseTag, self_closing=True): ...
