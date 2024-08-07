import pytest

from quickhtml.style import StyleSheet


@pytest.mark.parametrize(
    "style,expected_error",
    [
        ("color: red:", AssertionError),
        ("color: red", ValueError),
        ({"color": "red"}, ValueError),
    ],
)
def test_invalid_css_str(style, expected_error):
    with pytest.raises(expected_error):
        StyleSheet.from_css(style).render()


def test_from_css_dict():
    s = StyleSheet(ul={"color": "red", "width": 25})

    assert s.render() == (
        """ul {
    color: red;
    width: 25 px;
}
"""
    )


def test_css_combination():
    red = StyleSheet.from_css("color: red;")
    bold = StyleSheet.from_css("font-weight: bold;")
    red_bold = red + bold

    bolded_ul = StyleSheet(ul=red_bold)

    assert bolded_ul.render() == (
        """ul {
    color: red;
    font-weight: bold;
}
"""
    )


def test_css_nested():
    c = {
        "div": {
            "a:hover": {
                "font-weight": "bold",
            }
        }
    }
    s = StyleSheet(**c)

    assert s.render() == (
        """div a:hover {
    font-weight: bold;
}
"""
    )


def test_with_callable():
    def rounded(radius: int) -> StyleSheet:
        return StyleSheet(
            **{
                "border-radius": radius,
                "-moz-border-radius": int(round(radius * 1.5)),
                "-webkit-border-radius": int(round(radius * 2.0)),
            }
        )

    site_background = "#123450"
    red = StyleSheet.from_css("color: red;")
    blue = StyleSheet(color="blue")
    green = StyleSheet(**{"color": "green"})
    bold = StyleSheet.from_css("font-weight: bold;")
    red_bold = red + bold

    my_style = {
        ".blue": blue,
        ".green": green,
        "ul li": rounded(3)
        + blue
        + {
            "font-style": "italic",
            "background": site_background,
        },
        "div.ground": rounded(7)
        + red_bold
        + {
            "p": {
                "text-align": "left",
                "em": {
                    "font-size": "14pt",
                    "background": site_background,
                },
            },
        },
        "#my-id": green + red_bold,
    }
    s = StyleSheet(**my_style)

    assert s.render() == (
        """.blue {
    color: blue;
}
.green {
    color: green;
}
ul li {
    border-radius: 3 px;
    -moz-border-radius: 4 px;
    -webkit-border-radius: 6 px;
    color: blue;
    font-style: italic;
    background: #123450;
}
div.ground {
    border-radius: 7 px;
    -moz-border-radius: 10 px;
    -webkit-border-radius: 14 px;
    color: red;
    font-weight: bold;
}
div.ground p {
    text-align: left;
}
div.ground p em {
    font-size: 14pt;
    background: #123450;
}
#my-id {
    color: red;
    font-weight: bold;
}
"""
    )
