from __future__ import annotations

import typing
import inspect
import uvicorn

from starlette.applications import Starlette
from pathlib import Path

from rapidhtml.tags import Script
from rapidhtml.routing import RapidHTMLRouter, RapidHTMLWSEndpoint

JS_RELOAD_SCRIPT = """           
let active = false;
sock = new WebSocket(`ws://${window.location.host}/live-reload`);
sock.onopen = function (event) {
    console.log(`connected`);
    active = true;
};

sock.onclose = function (event) {
    console.log(`disconnected... reloading.`);
    if (active) {
        setTimeout(function () {
            location.reload();
            active = false;
        }, 5000);
    }
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
        self, *args, html_head: typing.Iterable = None, reload: bool = False, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.reload = reload
        self.html_head = (Script(src="https://unpkg.com/htmx.org@2.0.1"),) + tuple(
            html_head or ()
        )

        if reload:
            self.html_head += (Script(JS_RELOAD_SCRIPT),)
            self.router = RapidHTMLRouter(html_head=self.html_head)
            self.router.add_websocket_route("/live-reload", _ReloadSocket)
        else:
            self.router = RapidHTMLRouter(html_head=self.html_head)

    def serve(self, *args, **kwargs):
        appname = Path(inspect.currentframe().f_back.f_globals.get("__file__", "")).stem
        uvicorn.run(f"{appname}:app", reload=self.reload, *args, **kwargs)

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
