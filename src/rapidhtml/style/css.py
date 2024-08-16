from __future__ import annotations
from typing import Any, Generator, Union

from rapidhtml.tags import BaseTag


class StyleSheet(BaseTag):
    def __init__(self, **styles):
        super().__init__()

        self.__style_rules = styles

    @property
    def rules(self) -> dict:
        return self.__style_rules

    @classmethod
    def from_style(cls, css: str | dict) -> "StyleSheet":
        """
        Create a StyleSheet object from a valid Style attribute on a tag or a dictionary.

        Example:

        .. code-block:: python
            css = "color: red; font-size: 16px;"
            style = StyleSheet.from_css(css)
            print(style.rules)
            {'color': 'red', 'font-size': '16px'}

            Args:
                css (str | dict): The Style attribute data to parser or a dictionary containing style data.

            Returns:
                StyleSheet: The StyleSheet object.
        """
        if isinstance(css, str):
            k_v = {}
            for statement in css.split(";"):
                if not statement:
                    continue
                assert statement.count(":") == 1, f"Invalid CSS string '{statement}'"

                k, v = map(lambda x: x.strip(" :;\n"), statement.split(":"))
                k_v[k] = v

            return cls(**k_v)
        elif isinstance(css, dict):
            return cls(**css)

    def __add__(self, other: Union[dict, "StyleSheet"]) -> "StyleSheet":
        current_rules = self.rules

        if isinstance(other, StyleSheet):
            other_rules = other.rules
        elif isinstance(other, dict):
            other_rules = other

        return StyleSheet(**{**current_rules, **other_rules})

    def items(self) -> Generator[tuple[str, Any], None, None]:
        for name, value in self.rules.items():
            yield name, value

    def render(self, *, _nodes=None, _parent="", indent=4) -> str:
        """Given a dict mapping CSS selectors to a dict of styles, generate a
        list of lines of CSS output.

        Args:
            nodes (dist[str, str], optional): CSS selectors to render. If left empty, will use self.nodes. Defaults to None.
            _parent (str, optional): Used for recursive rendering. Defaults to "".
            _indent (int, optional): Used for recursive rendering. Defaults to 4.

            Example:
            .. code-block:: python
                   css = StyleSheet(
                       body={
                           "font-size": "16px",
                           "color": "red",
                       },
                       h1={
                           "font-size": "24px",
                           "color": "blue",
                       }
                   )
                   print(css.render())
                   # body {
                   #     font-size: 16px;
                   #     color: red;
                   # }
                   #
                   # h1 {
                   #     font-size: 24px;
                   #     color: blue;
                   # }
            Raises:
                TypeError: Raised if the value of a node is not a `dict`, `StyleSheet`, `str`, `int`, or `float`.
                ValueError: Raised if invalid CSS is provided.

            Returns:
                str: The rendered CSS document.
        """
        subnodes = []
        stylenodes = []

        current_nodes = _nodes or self.rules

        for name, value in current_nodes.items():
            # If the sub node is a nested style, we need to render it
            if isinstance(value, (dict, StyleSheet)):
                subnodes.append((name, value))

            # Else, it's a string, and thus, a single style element
            elif isinstance(value, (str, int, float)):
                stylenodes.append((name, value))
            else:
                raise TypeError(f"Invalid node type {type(value)}")

        if not subnodes and not _parent:
            raise ValueError("Invalid CSS!")

        ret_css = ""
        if stylenodes:
            ret_css += f"{_parent.strip()} {{\n"
            for name, value in stylenodes:
                name = name.rstrip(" ;:")
                if isinstance(value, str):
                    # string
                    value = value.rstrip(" ;:")
                else:
                    # everything else (int or float, likely)
                    value = f"{str(value)} px"
                ret_css += f"{' ' * indent}{name}: {value};\n"
            ret_css += "}\n\n"

        for subnode in subnodes:
            ret_css += self.render(
                _nodes=subnode[1],
                _parent=(_parent.strip() + " " + subnode[0]).strip(),
                indent=indent,
            )

        return ret_css
