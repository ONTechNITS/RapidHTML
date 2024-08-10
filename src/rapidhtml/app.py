from __future__ import annotations

import warnings
import typing
import inspect
import uvicorn
import socket
import logging
import asyncio
import logging.config

from starlette.applications import Starlette
from uvicorn.config import LOGGING_CONFIG
from pathlib import Path

from rapidhtml.tags import Script
from rapidhtml.routing import RapidHTMLRouter, RapidHTMLWSEndpoint

from __future__ import annotations

import asyncio
import logging
import os
import platform
import ssl
import sys
from configparser import RawConfigParser
from typing import IO, Any, Callable

import click

import uvicorn
from uvicorn._types import ASGIApplication
from uvicorn.config import (
    HTTP_PROTOCOLS,
    INTERFACES,
    LIFESPAN,
    LOG_LEVELS,
    LOGGING_CONFIG,
    LOOP_SETUPS,
    SSL_PROTOCOL_VERSION,
    WS_PROTOCOLS,
    Config,
    HTTPProtocolType,
    InterfaceType,
    LifespanType,
    LoopSetupType,
    WSProtocolType,
)
from uvicorn.server import Server, ServerState  # noqa: F401  # Used to be defined here.
from uvicorn.supervisors import ChangeReload, Multiprocess

LEVEL_CHOICES = click.Choice(list(LOG_LEVELS.keys()))
HTTP_CHOICES = click.Choice(list(HTTP_PROTOCOLS.keys()))
WS_CHOICES = click.Choice(list(WS_PROTOCOLS.keys()))
LIFESPAN_CHOICES = click.Choice(list(LIFESPAN.keys()))
LOOP_CHOICES = click.Choice([key for key in LOOP_SETUPS.keys() if key != "none"])
INTERFACE_CHOICES = click.Choice(INTERFACES)

STARTUP_FAILURE = 3

logger = logging.getLogger("rapidhtml.error")

JS_RELOAD_SCRIPT = """
const sock = new WebSocket(`ws://${window.location.host}/live-reload`);
sock.onopen = () => console.log(`Connected to the RapidHTML development server!`);
sock.onclose = () => {
    console.log(`disconnected... reloading.`);
    location.reload();
};
"""


# class uvicorn(uvicorn.Uvicorn):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     @classmethod
#     def run(cls, *args, **kwargs):
#
#
#
#         return super().run(*args, **kwargs)
#


def is_port_in_use(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


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

    """
    Initializes the RapidHTML application.

        Args:
            html_head (typing.Iterable, optional): Tags to inject into each 
                page's <head>. Defaults to None.
            reload (bool, optional): Enables live-reloading. Defaults to False.
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

    def serve(
        self,
        appname: str = None,
        host: str = "127.0.0.1",
        port: int = 8001,
        *args,
        **kwargs,
    ):
        if "reload" in kwargs:
            warnings.warn(
                "`reload` should be passed as an argument when initializing the app, not when serving the app.",
                UserWarning,
            )
            self.reload = kwargs.pop("reload")

        if self.reload:
            print(f"Running on http://{host}:{port} with live-reloading")
            caller_file = Path(
                inspect.currentframe().f_back.f_globals.get("__file__", "")
            )
            app = appname or caller_file.stem
            uvicorn.run(
                app=app, host=host, port=port, reload=self.reload, *args, **kwargs
            )
        else:
            print(f"Running on http://{host}:{port} without live-reloading")
            uvicorn.run(self, host=host, port=port, reload=self.reload, *args, **kwargs)

        print(f"Running {app} on http://{host}:{port}")
        if not is_port_in_use(host, port):
            uvicorn.run(
                app=app, host=host, port=port, reload=self.reload, *args, **kwargs
            )
        else:
            print(f"ERROR: Port {port} is already in use")

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
