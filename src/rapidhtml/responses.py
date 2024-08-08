from __future__ import annotations

import typing

from starlette.responses import Response

from rapidhtml.tags import BaseTag


class RapidHTMLResponse(Response):
    """
    RapidHTML Response. Renders the RapidHTML tags to HTML and sends the
    response to the client.
    """

    media_type = "text/html"

    def render(self, content: typing.Any) -> bytes:
        """
        Override the render method to render the RapidHTML tags to HTML.
        First check if the content is an instance of BaseTag, if so, render the
        content to HTML and encode it with the charset.

        Args:
            content (typing.Any): The content to render.

        Returns:
            bytes: The rendered content.
        """
        if isinstance(content, BaseTag):
            return content.render().encode(self.charset)
        return content
