from __future__ import annotations

import html
import inspect
import typing

from typing import Literal, Optional, Callable, Type

from rapidhtml.bases import Renderable
from rapidhtml.callbacks import RapidHTMLCallback
from rapidhtml.utils import get_app, dataclass_transform

if typing.TYPE_CHECKING:
    from rapidhtml import RapidHTML
    from starlette.applications import Starlette


T = typing.TypeVar("T")
BOOLEAN_ATTRS = [
    "autofocus",
    "checked",
    "disabled",
    "multiple",
    "readonly",
    "required",
    "webkitdirectory",
]


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


class BaseTag(BaseDataclass, Renderable):
    """
    Represents a base HTML tag.

    Args:
        *tags: Variable length arguments representing child tags.
        callback (typing.Callable | RapidHTMLCallback): A callback function to be added to the tag.
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
    callback: Optional[Callable] = None

    # Global attributes
    # https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes
    accesskey: Optional[str] = None
    class_: Optional[str] = None
    contenteditable: Optional[str] = None
    data: Optional[str] = None
    dir: Optional[str] = None
    draggable: Optional[str] = None
    enterkeyhint: Optional[str] = None
    hidden: Optional[str] = None
    id: Optional[str] = None
    inert: Optional[str] = None
    inputmode: Optional[str] = None
    lang: Optional[str] = None
    popover: Optional[str] = None
    spellcheck: Optional[str] = None
    style: Optional[str] = None
    tabindex: Optional[str] = None
    title: Optional[str] = None
    translate: Optional[str] = None
    
    # HTMX atrributes
    # https://htmx.org/reference/
    hx_get: Optional[str] = None
    hx_post: Optional[str] = None
    hx_delete: Optional[str] = None
    hx_patch: Optional[str] = None
    hx_put: Optional[str] = None
    hx_on: Optional[tuple[str, str]] = None
    hx_push_url: Optional[str] = None
    hx_select: Optional[str] = None
    hx_select_oob: Optional[str] = None
    hx_swap: Optional[
        Literal[
            "innerHTML",
            "outerHTML",
            "textContent",
            "beforebegin",
            "afterbegin",
            "beforeend",
            "afterend",
            "delete",
            "none",
        ]
    ] = "innerHTML"
    hx_swap_oob: Optional[
        Literal[
            "innerHTML",
            "outerHTML",
            "textContent",
            "beforebegin",
            "afterbegin",
            "beforeend",
            "afterend",
            "delete",
            "none",
        ]
    ] = None
    hx_target: Optional[str] = None
    hx_trigger: Optional[str] = None
    hx_vals: Optional[dict] = None
    hx_boost: Optional[bool] = None
    hx_confirm: Optional[str] = None
    hx_disable: Optional[bool] = None
    hx_disabled_elt: Optional[str] = None
    hx_disinherit: Optional[str] = None
    hx_encoding: Optional[str] = None
    hx_ext: Optional[str] = None
    hx_headers: Optional[dict] = None
    hx_history: Optional[bool] = None
    hx_history_elt: Optional[bool] = None
    hx_include: Optional[str] = None
    hx_indicator: Optional[str] = None
    hx_inherit: Optional[str] = None
    hx_params: Optional[str] = None
    hx_preserve: Optional[bool] = None
    hx_prompt: Optional[str] = None
    hx_replace_url: Optional[str] = None
    hx_request: Optional[str | dict] = None
    hx_sync: Optional[
        Literal[
            "drop",
            "abort",
            "replace",
            "queue",
            "queue first",
            "queue last",
            "queue all",
        ]
    ] = None
    hx_validate: Optional[bool] = None

    def __init__(
        self,
        *tags: "BaseTag" | str,
        callback: Callable | RapidHTMLCallback = None,
        **attrs,
    ):
        self.tag = self.__class__.__qualname__.lower().replace("htmltag", "")
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
    def tag_name(self) -> str:
        """
        Returns the name of the tag.

        Returns:
            str: The name of the tag.
        """
        return self.tag

    @property
    def app(self) -> "RapidHTML" | "Starlette":
        """
        Returns the current RapidHTML application instance.

        Returns:
            RapidHTML | Starlette: The current RapidHTML application instance.
        """
        return get_app()

    def add_callback(self, callback: Callable | RapidHTMLCallback):
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

    def add_head(self, *head: "BaseTag"):
        """
        Adds a head tag to the beginning of the list of child tags.

        Args:
            head: The head tag to be added.
        """
        if head:
            existing_head = self.pop("head", None)
            if existing_head:
                new_head = existing_head.tags + list(head)
            else:
                new_head = head
            self.tags.insert(0, Head(*new_head))

    def render(self):
        """
        Renders the HTML representation of the tag and its child tags.

        Returns:
            str: The HTML representation of the tag and its child tags.
        """

        ret_html = f"<{self.tag} "

        for key, value in self.attrs.items():
            key = key.rstrip("_")

            # Handle boolean attributes
            if key in BOOLEAN_ATTRS:
                ret_html += f"{key} "
                continue

            # Translate value None, True, or False to strings
            if value in (None, True, False):
                value = str(value).lower()

            # Replace underscores with hyphens
            key = key.replace("_", "-")
            ret_html += f"{key}='{value}' "

        if not self.__self_closing:
            ret_html = ret_html.rstrip() + ">"  # Take out trailing spaces

        # Recursively render child tags
        for tag in self.tags:
            if isinstance(tag, Renderable):
                ret_html += tag.render()
            elif hasattr(tag, "__str__"):
                ret_html += html.escape(str(tag))
            else:
                raise TypeError(f"Unexpected tag type {type(tag)}. {tag}")

        # Close the tag
        ret_html += self.__closing_tag

        return ret_html

    def select(
        self,
        select_tag: Type["BaseTag"] | str,
        *,
        recurse: bool = False,
        pop: bool = False,
        first_match: bool = False,
    ) -> list["BaseTag"]:
        """
        Selects and returns a list of BaseTag objects that match the given tag name or BaseTag object.

        Args:
            tag (Type[BaseTag] or str): The uninstantiated subclass of BaseTag or the tag name to match against.
            recurse (bool, optional): If True, recursively searches for matching tags within nested BaseTag objects. Defaults to False.
            pop (bool, optional): If True, removes the selected tags from the current object. Defaults to False.
            first_match (bool, optional): If True, stops searching after finding the first match. Defaults to False.

        Returns:
            list[BaseTag]: A list of BaseTag objects that match the given tag name or BaseTag object.

        Raises:
            KeyError: If no matching tags are found and pop is True.
            ValueError: If an instantiated object is passed as the tag parameter.
            TypeError: If the tag parameter is of an unexpected type.

        """
        if isinstance(select_tag, BaseTag):
            raise ValueError("Cannot pass instantiated object to select method!")
        elif inspect.isclass(select_tag) and issubclass(select_tag, BaseTag):
            select_tag_name = select_tag.__name__.lower()
        elif isinstance(select_tag, str):
            select_tag_name = select_tag.lower()
        else:
            raise TypeError(f"Unexpected tag type {type(select_tag)}. {select_tag}")

        ret_tags: list["BaseTag"] = []
        self_matches: list[tuple[int, "BaseTag"]] = []

        for i, tag in enumerate(self.tags):
            if not isinstance(tag, BaseTag):
                continue
            if tag.tag_name == select_tag_name:
                self_matches.append((i, tag))
                if first_match:
                    break
            elif recurse and isinstance(tag, BaseTag):
                sub_ret_tags = tag.select(
                    select_tag, recurse=recurse, pop=pop, first_match=first_match
                )
                if sub_ret_tags:
                    ret_tags.extend(sub_ret_tags)
                    if first_match:
                        break

        if not (ret_tags or self_matches) and pop:
            raise KeyError(f"Unable to find tag {select_tag}")

        # Pop in reverse order to avoid IndexError!
        for i, tag in sorted(self_matches, reverse=True, key=lambda tpl: tpl[0]):
            if pop:
                self.tags.pop(i)
            ret_tags.append(tag)

        return ret_tags

    def pop(self, tag: Type["BaseTag"] | str, *default: T) -> "BaseTag" | T:
        """
        Selects and removes the first occurrence of a tag that matches the given tag name or BaseTag object.
        If no matching tag is found, it returns the default value or raises a KeyError if no default is provided.

        Args:
            tag (Type[BaseTag] or str): The uninstantiated subclass of BaseTag or the tag name to match against.
            *default (typing.Optional[T]): typing.Optional default value to return if no matching tag is found. Defaults to None.

        Returns:
            BaseTag or T: The selected tag or the default value if no matching tag is found.

        Raises:
            KeyError: If no matching tags are found and no default value is provided.
            ValueError: If an instantiated object is passed as the tag parameter.
            TypeError: If the tag parameter is of an unexpected type.

        """
        if default and len(default) > 1:
            raise TypeError("pop expected at most 2 arguments, got more")
        try:
            return self.select(tag, pop=True, first_match=True)[0]
        except KeyError:
            if default:
                return default[0]
            raise


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
