Tag Callbacks
=============

Usage
-----

Creating a route for each action you want to perform in your application can 
quickly become cumbersome. To simplify this process, RapidHTML provides the
`callback` attribute on every tag that allows you to define a callback function
that will be called when the tag is interacted with. This callback function can
be used to perform any action that a standard route can perform, such as returning
a response or updating the page.

Here is an example that demonstrates how to use the `callback` attribute to define
a callback function for a button that updates the page with the current time when
clicked:

.. code-block:: python

    import datetime
    from rapidhtml import RapidHTML
    from rapidhtml.tags import *

    app = RapidHTML()

    async def update_time(request):
        return datetime.datetime.now().strftime("%H:%M:%S")

    @app.route("/")
    async def homepage(request):
        return Html(
                Div(
                    H1("Hello, world!"),
                    Button("Click me", id="button", 
                        callback=update_time, hx_target="#time"),
                    P(id="time"),
                )
            )

    app.serve()

In this example, the `update_time` function is defined as an asynchronous function
that returns the current time in the format `'%H:%M:%S'`. The `Button` element
is created with a `callback` attribute that is set to the `update_time` function.
When the button is clicked, the `update_time` function is called, and the `#time` 
tag's text is updated with the current time.

Behind the scenes, RapidHTML is using HTMX to send an AJAX request to the server
when the button is clicked, and the response from the server is used to update
the page. With that in mind, you can set any of the HTMX attributes on the button
element to customize the behaviour of the AJAX request.

By default, RapidHTML sets the `hx-get` attribute on the button element to the
route that the callback function is defined on.

You can read more about HTMX attributes in the 
`HTMX documentation <https://htmx.org/reference/>`_.

The `RapidHTMLCallback` class
-----------------------------

To make it easier to define callback functions, and allow you to send any type of
request you'd like, RapidHTML provides the `RapidHTMLCallback` class. This class
helps to abstract away the details of HTMX and allows you to define a callback
function that can return any type of response.

Here is an example that demonstrates how to use the `RapidHTMLCallback` class to
define a callback function for a button that updates the page with the current time
when clicked:

.. code-block:: python
    :emphasize-lines: 5, 15-19, 24

    import datetime
    from rapidhtml import RapidHTML
    from rapidhtml.tags import *

    from rapidhtml.callbacks import RapidHTMLCallback

    app = RapidHTML()

    async def update_time(request):
        return datetime.datetime.now().strftime("%H:%M:%S")

    @app.route("/")
    async def homepage(request):

        time_callback = RapidHTMLCallback(
            func=update_time,
            method="post",
            target="#time"
        )

        return Html(
                Div(
                    H1("Hello, world!"),
                    Button("Click me", id="button", callback=time_callback),
                    P(id="time"),
                )
            )

    app.serve()

