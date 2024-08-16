from __future__ import annotations

import typing
import inspect
import warnings

from pathlib import Path

import uvicorn

from starlette.applications import Starlette
from starlette.responses import FileResponse, Response

from rapidhtml.tags import Script, Title
from rapidhtml.utils import get_default_favicon
from rapidhtml.routing import RapidHTMLRouter, RapidHTMLWSEndpoint


JS_RELOAD_SCRIPT = """
const sock = new WebSocket(`ws://${window.location.host}/live-reload`);
sock.onopen = () => console.log(`Connected to the RapidHTML development server!`);
sock.onclose = () => {
    console.log(`disconnected... reloading.`);
    location.reload();
};
"""


class _ReloadSocket(RapidHTMLWSEndpoint):
    encoding = "text"

    async def on_connect(self, websocket):
        await websocket.accept()


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
        reload: bool = False,
        title: str = "RapidHTML",
        favicon_path: str | Path = None,
        **kwargs,
    ) -> None:
        """
        Initializes the RapidHTML application.

            Args:
                html_head (typing.Iterable, optional): Tags to inject into each
                    page's <head>. Defaults to None.
                reload (bool, optional): Enables live-reloading. Defaults to False.
                title (str, optional): Title of the application. Can be overridden
                    on a per-page basis by adding a Title() tag to the response.
                    Defaults to "RapidHTML".
                favicon_path (str | Path, optional): Path to the desired
                    favicon. If no path is provided the default RapidHTML favicon
                    will be used instead.
                    Defaults to None.
        """
        super().__init__(*args, **kwargs)

        self.reload = reload
        self.favicon_path = favicon_path
        self.html_head = (
            Title(title),
            Script(src="https://unpkg.com/htmx.org@2.0.1"),
        ) + tuple(html_head or ())

        if reload:
            self.html_head += (Script(JS_RELOAD_SCRIPT),)
            self.router = RapidHTMLRouter(html_head=self.html_head)
            self.router.add_websocket_route("/live-reload", _ReloadSocket)
        else:
            self.router = RapidHTMLRouter(html_head=self.html_head)

        # Get the favicon and store it
        if favicon_path is None:
            self.favicon_data = get_default_favicon()
        else:
            with open(favicon_path, "rb") as f:
                self.favicon_data = f.read()

        @self.route("/favicon.ico")
        async def favicon_route():
            nonlocal self
            return Response(self.favicon_data, media_type="image/svg+xml")

    def serve(self, appname=None, *args, **kwargs):
        if "reload" in kwargs:
            warnings.warn(
                "`reload` should be passed as an argument when initializing the app, not when serving the app.",
                UserWarning,
            )
            self.reload = kwargs.pop("reload")

        caller_file = Path(inspect.currentframe().f_back.f_globals.get("__file__", ""))
        app = f"{appname or caller_file.stem}:app" if self.reload else self
        uvicorn.run(app=app, reload=self.reload, *args, **kwargs)

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
