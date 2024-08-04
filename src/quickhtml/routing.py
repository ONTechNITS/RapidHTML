from __future__ import annotations

import typing
import inspect

from starlette.requests import Request
from starlette.routing import Route, Router
from starlette.responses import JSONResponse, PlainTextResponse, Response

from quickhtml.tags import BaseTag
from quickhtml.responses import QuickHTMLResponse


class QuickHTMLRoute(Route):
    """
    QuickHTML Route. Extends the Starlette Route to include an endpoint
    override that will render the response to HTML if the response is an
    instance of BaseTag. If the response is a dict, it will be converted to a
    JSONResponse. If the response is a string, it will be converted to a
    PlainTextResponse.
    """

    def __init__(self, *args, html_head: typing.Iterable = None, **kwargs) -> None:
        self.endpoint_func = kwargs.pop("endpoint", None)
        super().__init__(*args, endpoint=self.endpoint_override, **kwargs)
        self.html_head = html_head

    async def endpoint_override(self, request: Request) -> Response:
        """
        Overrides the default endpoint behaviour and returns a modified response.

        Args:
            request (Request): The incoming request object.

        Returns:
            Response: The modified response object.
        """
        # I hate having to include `request` in every route, so let's give
        # the option to not
        if "request" in inspect.signature(self.endpoint_func).parameters:
            response = await self.endpoint_func(request=request)
        else:
            response = await self.endpoint_func()

        # Handle different response types
        if isinstance(response, BaseTag):
            response.add_head(self.html_head)
            response = QuickHTMLResponse(response)
        elif isinstance(response, dict):
            response = JSONResponse(response)
        elif isinstance(response, str):
            response = PlainTextResponse(response)
        elif response is None:
            response = Response()
        return response


class QuickHTMLRouter(Router):
    """
    A custom router class for handling QuickHTML routes.

    Args:
        *args: Variable length argument list.
        html_head (typing.Iterable, optional): An iterable containing HTML head
            elements. Defaults to None.
        **kwargs: Arbitrary keyword arguments.

    Attributes:
        html_head (typing.Iterable): An iterable containing HTML head elements.

    Methods:
        add_route: Add a route to the router.

    Inherits:
        Router: The base router class.

    """

    def __init__(self, *args, html_head: typing.Iterable = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.html_head = html_head

    def add_route(
        self,
        path: str,
        endpoint: typing.Callable[[Request], typing.Awaitable[Response] | Response],
        methods: list[str] | None = None,
        name: str | None = None,
        include_in_schema: bool = True,
    ) -> None:  # pragma: nocover
        """
        Add a route to the routing table.

        Args:
            path (str): The URL path pattern for the route.
            endpoint (typing.Callable[[Request], typing.Awaitable[Response] | Response]):
                The function or coroutine that handles the route.
            methods (list[str] | None, optional): The HTTP methods allowed for the route.
                Defaults to None.
            name (str | None, optional): The name of the route. Defaults to None.
            include_in_schema (bool, optional): Whether to include the route in the API schema.
                Defaults to True.

        Returns:
            None: This method does not return anything.
        """
        route = QuickHTMLRoute(
            path,
            html_head=self.html_head,
            endpoint=endpoint,
            methods=methods,
            name=name,
            include_in_schema=include_in_schema,
        )
        self.routes.append(route)
