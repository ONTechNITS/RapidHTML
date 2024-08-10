from __future__ import annotations

import typing
import pathlib

import uvicorn

from starlette.applications import Starlette
from starlette.responses import FileResponse, Response

from rapidhtml.tags import Script, Title
from rapidhtml.routing import RapidHTMLRouter
from rapidhtml.utils import get_default_favicon


class RapidHTML(Starlette):
    """
    RapidHTML Application. Extends the Starlette application to include
    the RapidHTMLRouter. Additionally allows for the inclusion of HTML head
    tags to be included in the response along with default head content.

    Default head content includes:
        - HTMX
    """

    def __init__(
        self,
        *args,
        html_head: typing.Iterable = None,
        title: str = "RapidHTML",
        favicon_path: str | pathlib.Path = None,
        **kwargs,
    ) -> None:
        """The RapidHTML Application.

        Args:
            html_head (typing.Iterable, optional): Extra tags to put into each
                pages <head>.
                Defaults to None.
            title (str, optional): Title of the application. Can be overridden
                on a per-page basis by adding a Title() tag to the response.
                Defaults to "RapidHTML".
            favicon_path (str | pathlib.Path, optional): Path to the desired
                favicon. If no path is provided the default RapidHTML favicon
                will be used instead.
                Defaults to None.

        """
        super().__init__(*args, **kwargs)
        if not html_head:
            html_head = ()
        self.html_head = [
            Title(title),
            Script(src="https://unpkg.com/htmx.org@2.0.1"),
        ]
        self.html_head.extend(html_head)
        self.router = RapidHTMLRouter(html_head=self.html_head)

        self.favicon_path = favicon_path

        @self.route("/favicon.ico")
        async def favicon_route():
            nonlocal favicon_path

            if favicon_path is None:
                return Response(get_default_favicon(), media_type="image/svg+xml")

            with open(favicon_path, "rb") as f:
                return FileResponse(f.read())

    def serve(self, *args, **kwargs):
        uvicorn.run(self, *args, **kwargs)

    def route(self, path, *args, **kwargs):
        def decorator(cls):
            self.router.add_route(path, cls, *args, **kwargs)
            return cls

        return decorator

    def websocket_route(self, path, *args, **kwargs):
        def decorator(cls):
            self.router.add_websocket_route(path, cls, *args, **kwargs)
            return cls

        return decorator
