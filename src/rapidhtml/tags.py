from __future__ import annotations

import html
import typing

from collections.abc import Iterable

from rapidhtml.callbacks import RapidHTMLCallback
from rapidhtml.style import StyleSheet
from rapidhtml.utils import get_app

if typing.TYPE_CHECKING:
    from rapidhtml import RapidHTML
    from starlette.applications import Starlette


class BaseTag:
    """
    Represents a base HTML tag.

    Args:
        *tags: Variable length arguments representing child tags.
        callback (typing.Callable | QuickHTMLCallback): A callback function to be added to the tag.
        **attrs: Keyword arguments representing tag attributes.

    Attributes:
        tag (str): The name of the HTML tag.
        tags (list): A list of child tags.
        attrs (dict): A dictionary of tag attributes.

    Methods:
        add_head(head): Adds a head tag to the beginning of the list of child tags.
        render(): Renders the HTML representation of the tag and its child tags.
    """

    def __init__(
        self, *tags, callback: typing.Callable | RapidHTMLCallback = None, **attrs
    ):
        self.tag = self.__class__.__qualname__.lower().replace("htmltag", "")
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
    def app(self) -> "RapidHTML" | "Starlette":
        """
        Returns the current RapidHTML application instance.

        Returns:
            RapidHTML | Starlette: The current RapidHTML application instance.
        """
        return get_app()

    def add_callback(self, callback: typing.Callable | RapidHTMLCallback):
        """
        Adds a callback function to the tag.

        Args:
            callback (typing.Callable): The callback function to be added.
        """
        method = "get"
        if isinstance(callback, RapidHTMLCallback):
            callback, method, attrs = callback.get_data()
            self.attrs.update(attrs)

        self.callback_route = f"/python-callbacks/{id(callback)}"

        self.app.add_route(self.callback_route, callback, [method])

        self.attrs[f"hx-{method}"] = self.callback_route

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

            if value is True:
                ret_html += f"{key} "
                continue

            # Replace underscores with hyphens
            key = key.replace("_", "-")
            ret_html += f"{key}='{value}' "

        if not self.__self_closing:
            ret_html = ret_html.rstrip() + ">"  # Take out trailing spaces

        # Recursively render child tags
        for tag in self.tags:
            if isinstance(tag, (BaseTag, StyleSheet)):
                ret_html += tag.render()
            elif hasattr(tag, "__str__"):
                ret_html += html.escape(str(tag))
            else:
                raise TypeError(f"Unexpected tag type {type(tag)}. {tag}")

        # Close the tag
        ret_html += self.__closing_tag

        return ret_html


class HtmlTagA(BaseTag): ...


class Abbr(BaseTag): ...


class Address(BaseTag): ...


class Area(BaseTag, self_closing=True): ...


class Article(BaseTag): ...


class Aside(BaseTag): ...


class Audio(BaseTag): ...


class HtmlTagB(BaseTag): ...


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


class HtmlTagI(BaseTag): ...


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


class HtmlTagP(BaseTag): ...


class Picture(BaseTag): ...


class PortalExperimental(BaseTag): ...


class Pre(BaseTag): ...


class Progress(BaseTag): ...


class HtmlTagQ(BaseTag): ...


class Rp(BaseTag): ...


class Rt(BaseTag): ...


class Ruby(BaseTag): ...


class HtmlTagS(BaseTag): ...


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


class HtmlTagU(BaseTag): ...


class Ul(BaseTag): ...


class Var(BaseTag): ...


class Video(BaseTag): ...


class Wbr(BaseTag, self_closing=True): ...


A = HtmlTagA
B = HtmlTagB
I = HtmlTagI  # noqa
P = HtmlTagP
Q = HtmlTagQ
S = HtmlTagS
U = HtmlTagU

__all__ = (
    "A",
    "Abbr",
    "Address",
    "Area",
    "Article",
    "Aside",
    "Audio",
    "B",
    "Base",
    "Bdi",
    "Bdo",
    "Blockquote",
    "Body",
    "Br",
    "Button",
    "Canvas",
    "Caption",
    "Cite",
    "Code",
    "Col",
    "Colgroup",
    "Data",
    "Datalist",
    "Dd",
    "Del",
    "Details",
    "Dfn",
    "Dialog",
    "Div",
    "Dl",
    "Dt",
    "Em",
    "Embed",
    "Fencedframe",
    "Fieldset",
    "Figcaption",
    "Figure",
    "Footer",
    "Form",
    "H1",
    "Head",
    "Header",
    "Hgroup",
    "Hr",
    "Html",
    "I",
    "Iframe",
    "Img",
    "Input",
    "Ins",
    "Kbd",
    "Label",
    "Legend",
    "Li",
    "Link",
    "Main",
    "Map",
    "Mark",
    "Menu",
    "Meta",
    "Meter",
    "Nav",
    "Noscript",
    "Object",
    "Ol",
    "Optgroup",
    "Option",
    "Output",
    "P",
    "Picture",
    "PortalExperimental",
    "Pre",
    "Progress",
    "Q",
    "Rp",
    "Ruby",
    "S",
    "Samp",
    "Script",
    "Search",
    "Section",
    "Select",
    "Slot",
    "Small",
    "Source",
    "Span",
    "Strong",
    "Style",
    "Sub",
    "Summary",
    "Sup",
    "Table",
    "Tbody",
    "Td",
    "Template",
    "Textarea",
    "Tfoot",
    "Th",
    "Thead",
    "Time",
    "Title",
    "Tr",
    "Track",
    "U",
    "Ul",
    "Var",
    "Video",
    "Wbr",
)
