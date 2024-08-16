import pathlib

import pytest

from starlette.testclient import TestClient

from rapidhtml import RapidHTML
from rapidhtml.tags import Html, H1, Div
from rapidhtml.utils import get_default_favicon


@pytest.fixture
def app():
    return RapidHTML()


@pytest.fixture
def client(app):
    @app.route("/")
    async def homepage(request):
        return Html(
            Div(
                H1("foobar"),
            )
        )

    return TestClient(app)


def test_app(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>RapidHTML</title>" in response.text
    assert "<h1>foobar</h1>" in response.text
    assert "htmx.org" in response.text


def test_favicon(client):
    response = client.get("/favicon.ico")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/svg+xml"
    assert response.content == get_default_favicon()


def test_user_favicon():
    path = pathlib.Path(__file__).parent
    app = RapidHTML(favicon_path=f"{path}/../src/rapidhtml/static/RapidHTML.svg")
    client = TestClient(app)
    response = client.get("/favicon.ico")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/svg+xml"
    assert response.content == get_default_favicon()
