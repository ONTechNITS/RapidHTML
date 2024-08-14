from __future__ import annotations

import html
import inspect
import typing

from rapidhtml.utils import get_app

if typing.TYPE_CHECKING:
    from rapidhtml import RapidHTML
    from starlette.applications import Starlette


T = typing.TypeVar("T")


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

    def __init__(
        self, *tags: "BaseTag" | str, callback: typing.Callable = None, **attrs
    ):
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
            if isinstance(tag, BaseTag):
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
        select_tag: typing.Type["BaseTag"] | str,
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
            select_tag_name = select_tag
        else:
            raise TypeError(f"Unexpected tag type {type(select_tag)}. {select_tag}")

        ret_tags: list["BaseTag"] = []
        self_matches: list[tuple[int, "BaseTag"]] = []

        for i, tag in enumerate(self.tags):
            if not isinstance(tag, BaseTag):
                continue
            tag_name = tag.tag_name
            if tag_name == select_tag_name or tag_name == f"htmltag{select_tag_name}":
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

    def pop(self, tag: typing.Type["BaseTag"] | str, *default: T) -> "BaseTag" | T:
        """
        Selects and removes the first occurrence of a tag that matches the given tag name or BaseTag object.
        If no matching tag is found, it returns the default value or raises a KeyError if no default is provided.

        Args:
            tag (Type[BaseTag] or str): The uninstantiated subclass of BaseTag or the tag name to match against.
            *default (Optional[T]): Optional default value to return if no matching tag is found. Defaults to None.

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


class H2(BaseTag): ...


class H3(BaseTag): ...


class H4(BaseTag): ...


class H5(BaseTag): ...


class H6(BaseTag): ...


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
