import pytest

from starlette.testclient import TestClient

from rapidhtml import RapidHTML
from rapidhtml.tags import Html, H1, Body, Title, BaseDataclass


def test_render():
    test_html = Html(
        Body(
            H1("foobar"),
        )
    )

    expected_html = "<html><body><h1>foobar</h1></body></html>"
    assert test_html.render() == expected_html


def test_render_with_attributes():
    test_html = Html(
        Body(
            H1("foobar", id="foo", class_="bar"),
        )
    )

    expected_html = "<html><body><h1 id='foo' class='bar'>foobar</h1></body></html>"
    assert test_html.render() == expected_html


def test_render_with_head():
    # Test with a single tag
    test_html = Html(
        Body(
            H1("foobar"),
        )
    )

    test_html.add_head(Title("foobar"))
    expected_html = (
        "<html><head><title>foobar</title></head><body><h1>foobar</h1></body></html>"
    )
    assert test_html.render() == expected_html

    # Test with a tuple of tags
    test_html = Html(
        Body(
            H1("foobar"),
        )
    )

    test_html.add_head((Title("foobar"),))
    expected_html = (
        "<html><head><title>foobar</title></head><body><h1>foobar</h1></body></html>"
    )
    assert test_html.render() == expected_html


def test_tag_name():
    test_html = Html()
    assert test_html.tag == "html"

    test_body = Body()
    assert test_body.tag == "body"

    test_h1 = H1()
    assert test_h1.tag == "h1"


def test_tag_callback():
    async def callback():
        return "Callback"

    test_app = RapidHTML()

    test_html = Html(callback=callback)
    assert test_html.attrs["hx-get"] == "/python-callbacks/{}".format(id(callback))

    client = TestClient(test_app)
    response = client.get(test_html.attrs["hx-get"])
    assert response.text == "Callback"


def test_base_dataclass():
    class Parent(BaseDataclass):
        a: str = None
        b: int = None

    assert Parent().__annotations__ == {"a": str, "b": int}

    class Child(Parent):
        c: str = None

    assert Child().__annotations__ == {"a": str, "b": int, "c": str}

    child = Child(a="a", b=1, c="c")
    assert child.a == "a"
    assert child.b == 1
    assert child.c == "c"

    child = Child()
    assert child.a == None
    assert child.b == None
    assert child.c == None

    with pytest.raises(AttributeError):
        Child(d="d")
