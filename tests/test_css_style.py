import pytest

from quickhtml.style import Style


@pytest.mark.parametrize(
    "style,expected_error",
    [
        ("color: red:", AssertionError),
        ("color: red", ValueError),
    ],
)
def test_invalid_css_str(style, expected_error):
    with pytest.raises(expected_error):
        Style.from_css(style).render()


def test_from_css_str():
    s = Style(ul={"color": "red", "width": 25})

    assert (
        s.render()
        == """ul {
     color: red;
     width: 25 px;
}
"""
    )
