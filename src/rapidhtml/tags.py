from __future__ import annotations

import html
import typing
import inspect

from collections.abc import Iterable

from rapidhtml.style import StyleSheet
from rapidhtml.utils import get_app, dataclass_transform

if typing.TYPE_CHECKING:
    from rapidhtml import RapidHTML
    from starlette.applications import Starlette


@dataclass_transform()
class BaseDataclass:
    """
    Base dataclass tranformations class. Used to typehint tags when using
    Python3.11+
    """

    def __init_subclass__(cls, **kwargs):
        def func(cls, *args, **kwargs):
            # Create a new object instance
            obj = super().__new__(cls)

            # Go up the MRO tree, grabbing and update annotations as necessary
            for c in inspect.getmro(obj.__class__):
                if c is object:
                    continue
                if not hasattr(c, "__annotations__"):
                    setattr(c, "__annotations__", {})
                obj.__annotations__.update(c.__annotations__)

            # Go through the kwargs add set their values
            for key, value in kwargs.items():
                if key in obj.__annotations__:
                    setattr(obj, key, value)
                    continue
                raise AttributeError(f"{key} is not a defined attribute")

            # Return the object
            return obj

        # Make this the __new__ method so that we can define our __init__ freely
        cls.__new__ = func


class BaseTag(BaseDataclass):
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

    # RapidHTML attributes
    callback: typing.Callable = None

    # Global attributes
    # https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes
    accesskey: str = None
    class_: str = None
    contenteditable: str = None
    data: str = None
    dir: str = None
    draggable: str = None
    enterkeyhint: str = None
    hidden: str = None
    id: str = None
    inert: str = None
    inputmode: str = None
    lang: str = None
    popover: str = None
    spellcheck: str = None
    style: str = None
    tabindex: str = None
    title: str = None
    translate: str = None

    def __init__(self, *tags, callback: typing.Callable = None, **attrs):
        self.tag = self.__class__.__qualname__.lower()
        self.tags = list(tags)
        self.attrs = attrs
        self.callback = callback
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


class HtmlTagA(BaseTag):
    download: str = None
    href: str = None
    hreflang: str = None
    media: str = None
    ping: str = None
    referrerpolicy: str = None
    rel: str = None
    shape: str = None
    target: str = None


class Abbr(BaseTag): ...


class Address(BaseTag): ...


class Area(BaseTag, self_closing=True):
    alt: str = None
    coords: str = None
    download: str = None
    href: str = None
    media: str = None
    ping: str = None
    referrerpolicy: str = None
    rel: str = None
    shape: str = None
    target: str = None


class Article(BaseTag): ...


class Aside(BaseTag): ...


class Audio(BaseTag):
    autoplay: str = None
    controls: str = None
    crossorigin: str = None
    loop: str = None
    muted: str = None
    preload: str = None
    src: str = None


class HtmlTagB(BaseTag): ...


class Base(BaseTag, self_closing=True):
    href: str = None
    target: str = None


class Bdi(BaseTag): ...


class Bdo(BaseTag): ...


class Blockquote(BaseTag):
    cite: str = None


class Body(BaseTag):
    background: str = None
    bgcolor: str = None


class Br(BaseTag, self_closing=True): ...


class Button(BaseTag):
    disabled: str = None
    form: str = None
    formaction: str = None
    formenctype: str = None
    formmethod: str = None
    formnovalidate: str = None
    formtarget: str = None
    name: str = None
    type: str = None
    value: str = None


class Canvas(BaseTag):
    height: str = None
    width: str = None


class Caption(BaseTag): ...


class Cite(BaseTag): ...


class Code(BaseTag): ...


class Col(BaseTag, self_closing=True):
    bgcolor: str = None
    span: str = None


class Colgroup(BaseTag):
    bgcolor: str = None
    span: str = None


class Data(BaseTag):
    value: str = None


class Datalist(BaseTag): ...


class Dd(BaseTag): ...


class Del(BaseTag):
    cite: str = None
    datetime: str = None


class Details(BaseTag):
    open: str = None


class Dfn(BaseTag): ...


class Dialog(BaseTag):
    open: str = None


class Div(BaseTag): ...


class Dl(BaseTag): ...


class Dt(BaseTag): ...


class Em(BaseTag): ...


class Embed(BaseTag, self_closing=True):
    height: str = None
    src: str = None
    type: str = None
    width: str = None


class Fencedframe(BaseTag): ...


class Fieldset(BaseTag):
    disabled: str = None
    form: str = None
    name: str = None


class Figcaption(BaseTag): ...


class Figure(BaseTag): ...


class Footer(BaseTag): ...


class Form(BaseTag):
    accept: str = None
    accept_charset: str = None
    action: str = None
    autocomplete: str = None
    enctype: str = None
    method: str = None
    name: str = None
    novalidate: str = None
    target: str = None


class H1(BaseTag): ...


class H2(BaseTag): ...


class H3(BaseTag): ...


class H4(BaseTag): ...


class H5(BaseTag): ...


class H6(BaseTag): ...


class Head(BaseTag): ...


class Header(BaseTag): ...


class Hgroup(BaseTag): ...


class Hr(BaseTag, self_closing=True):
    color: str = None


class Html(BaseTag): ...


class HtmlTagI(BaseTag): ...


class Iframe(BaseTag):
    allow: str = None
    height: str = None
    loading: str = None
    name: str = None
    referrerpolicy: str = None
    sandbox: str = None
    src: str = None
    srcdoc: str = None
    width: str = None


class Img(BaseTag, self_closing=True):
    alt: str = None
    border: str = None
    crossorigin: str = None
    decoding: str = None
    height: str = None
    ismap: str = None
    loading: str = None
    referrerpolicy: str = None
    sizes: str = None
    src: str = None
    srcset: str = None
    usemap: str = None
    width: str = None


class Input(BaseTag, self_closing=True):
    accept: str = None
    alt: str = None
    autocomplete: str = None
    capture: str = None
    checked: str = None
    dirname: str = None
    disabled: str = None
    form: str = None
    formaction: str = None
    formenctype: str = None
    formmethod: str = None
    formnovalidate: str = None
    formtarget: str = None
    height: str = None
    list: str = None
    max: str = None
    maxlength: str = None
    minlength: str = None
    min: str = None
    multiple: str = None
    name: str = None
    pattern: str = None
    placeholder: str = None
    readonly: str = None
    required: str = None
    size: str = None
    src: str = None
    step: str = None
    type: str = None
    usemap: str = None
    value: str = None
    width: str = None


class Ins(BaseTag):
    cite: str = None
    datetime: str = None


class Kbd(BaseTag): ...


class Label(BaseTag):
    for_: str = None
    form: str = None


class Legend(BaseTag): ...


class Li(BaseTag):
    value: str = None


class Link(BaseTag, self_closing=True):
    as_: str = None
    crossorigin: str = None
    href: str = None
    hreflang: str = None
    integrity: str = None
    media: str = None
    referrerpolicy: str = None
    rel: str = None
    sizes: str = None
    type: str = None


class Main(BaseTag): ...


class Map(BaseTag):
    name: str = None


class Mark(BaseTag): ...


class Marquee(BaseTag):
    bgcolor: str = None
    loop: str = None


class Menu(BaseTag):
    type: str = None


class Meta(BaseTag, self_closing=True):
    charset: str = None
    content: str = None
    http_equiv: str = None
    name: str = None


class Meter(BaseTag):
    form: str = None
    high: str = None
    low: str = None
    max: str = None
    min: str = None
    optimum: str = None
    value: str = None


class Nav(BaseTag): ...


class Noscript(BaseTag): ...


class Object(BaseTag):
    border: str = None
    data: str = None
    form: str = None
    height: str = None
    name: str = None
    type: str = None
    usemap: str = None
    width: str = None


class Ol(BaseTag):
    reversed: str = None
    start: str = None
    type: str = None


class Optgroup(BaseTag):
    disabled: str = None
    label: str = None


class Option(BaseTag):
    disabled: str = None
    label: str = None
    selected: str = None
    value: str = None


class Output(BaseTag):
    for_: str = None
    form: str = None
    name: str = None


class HtmlTagP(BaseTag): ...


class Picture(BaseTag): ...


class PortalExperimental(BaseTag): ...


class Pre(BaseTag): ...


class Progress(BaseTag):
    form: str = None
    max: str = None
    value: str = None


class HtmlTagQ(BaseTag):
    cite: str = None


class Rp(BaseTag): ...


class Rt(BaseTag): ...


class Ruby(BaseTag): ...


class HtmlTagS(BaseTag): ...


class Samp(BaseTag): ...


class Script(BaseTag):
    async_: str = None
    crossorigin: str = None
    defer: str = None
    integrity: str = None
    referrerpolicy: str = None
    src: str = None
    type: str = None


class Search(BaseTag): ...


class Section(BaseTag): ...


class Select(BaseTag):
    autocomplete: str = None
    disabled: str = None
    form: str = None
    multiple: str = None
    name: str = None
    required: str = None
    size: str = None


class Slot(BaseTag): ...


class Small(BaseTag): ...


class Source(BaseTag, self_closing=True):
    media: str = None
    sizes: str = None
    src: str = None
    srcset: str = None
    type: str = None


class Span(BaseTag): ...


class Strong(BaseTag): ...


class Style(BaseTag):
    media: str = None
    type: str = None


class Sub(BaseTag): ...


class Summary(BaseTag): ...


class Sup(BaseTag): ...


class Table(BaseTag):
    background: str = None
    bgcolor: str = None
    border: str = None


class Tbody(BaseTag):
    bgcolor: str = None


class Td(BaseTag):
    background: str = None
    bgcolor: str = None
    colspan: str = None
    headers: str = None
    rowspan: str = None


class Template(BaseTag): ...


class Textarea(BaseTag):
    autocomplete: str = None
    cols: str = None
    dirname: str = None
    disabled: str = None
    enterkeyhint: str = None
    form: str = None
    inputmode: str = None
    maxlength: str = None
    minlength: str = None
    name: str = None
    placeholder: str = None
    readonly: str = None
    required: str = None
    rows: str = None


class Tfoot(BaseTag):
    bgcolor: str = None


class Th(BaseTag):
    background: str = None
    bgcolor: str = None
    colspan: str = None
    headers: str = None
    rowspan: str = None
    scope: str = None


class Thead(BaseTag): ...


class Time(BaseTag):
    datetime: str = None


class Title(BaseTag): ...


class Tr(BaseTag):
    bgcolor: str = None


class Track(BaseTag, self_closing=True):
    default: str = None
    kind: str = None
    label: str = None
    src: str = None
    srclang: str = None


class HtmlTagU(BaseTag): ...


class Ul(BaseTag): ...


class Var(BaseTag): ...


class Video(BaseTag):
    autoplay: str = None
    controls: str = None
    crossorigin: str = None
    height: str = None
    loop: str = None
    muted: str = None
    playsinline: str = None
    poster: str = None
    preload: str = None
    src: str = None
    width: str = None


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
    "H2",
    "H3",
    "H4",
    "H5",
    "H6",
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
