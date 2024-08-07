from __future__ import annotations
from typing import Any, Generator, Union


class StyleSheet:
    def __init__(self, **styles):
        self.__style_rules = styles

    @property
    def rules(self) -> dict:
        return self.__style_rules

    @classmethod
    def from_css(cls, css: str | dict):
        if isinstance(css, str):
            k_v = {}
            for statement in css.split(";"):
                if not statement:
                    continue
                assert statement.count(":") == 1, f"Invalid CSS string '{css}'"

                k, v = map(lambda x: x.strip(" :;\n"), css.split(":"))
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

    def render(self, nodes=None, parent="", indent=4) -> str:
        """Given a dict mapping CSS selectors to a dict of styles, generate a
        list of lines of CSS output."""
        subnodes = []
        stylenodes = []

        current_nodes = nodes or self.rules

        for name, value in current_nodes.items():
            # If the sub node is a nested style, we need to render it
            if isinstance(value, (dict, StyleSheet)):
                subnodes.append((name, value))

            # Else, it's a string, and thus, a single style element
            elif isinstance(value, (str, int, float)):
                stylenodes.append((name, value))
            else:
                raise TypeError(f"Invalid node type {type(value)}")

        if not subnodes and not parent:
            raise ValueError("Invalid CSS!")

        ret_css = ""
        if stylenodes:
            ret_css += f"{parent.strip()} {{\n"
            for stylenode in stylenodes:
                attribute = stylenode[0].rstrip(" ;:")
                if isinstance(stylenode[1], str):
                    # string
                    value = stylenode[1].rstrip(" ;:")
                else:
                    # everything else (int or float, likely)
                    value = f"{str(stylenode[1])} px"
                ret_css += f"{' ' * indent}{attribute}: {value};\n"
            ret_css += "}\n"

        for subnode in subnodes:
            ret_css += self.render(
                subnode[1], parent=(parent.strip() + " " + subnode[0]).strip()
            )

        return ret_css
