from __future__ import annotations

import typing

import uvicorn

from starlette.applications import Starlette

from quickhtml.tags import Script
from quickhtml.routing import QuickHTMLRouter


class QuickHTML(Starlette):
    """
    QuickHTML Application. Extends the Starlette application to include
    the QuickHTMLRouter. Additionally allows for the inclusion of HTML head
    tags to be included in the response along with default head content.

    Default head content includes:
        - HTMX
    """

    def __init__(self, *args, html_head: typing.Iterable = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not html_head:
            html_head = ()
        self.html_head = (Script(src="https://unpkg.com/htmx.org@2.0.1"),) + tuple(
            html_head
        )
        self.router = QuickHTMLRouter(html_head=self.html_head)

    def serve(self, *args, **kwargs):
        uvicorn.run(self, *args, **kwargs)