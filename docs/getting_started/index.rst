Getting Started
===============

Welcome to the Getting Started guide for the `QuickHTML` project! This guide will
walk you through the process of creating a simple QuickHTML application.

Installation
------------
To install QuickHTML, you can use `pip`:

.. code-block:: bash

    pip install quickhtml

Creating a QuickHTML Application
--------------------------------

To create a QuickHTML application, you need to create an instance of the `QuickHTML`
class and define routes using the `route` decorator. Here is an example of a simple
QuickHTML application that serves a single page with a button that, when clicked,
sends an AJAX request to the server and updates the page with the response broken down into steps:

1. Import the `QuickHTML` class and the `tags` module:

.. code-block:: python

    from quickhtml import QuickHTML
    from quickhtml.tags import *

2. Create an instance of the `QuickHTML` class:

.. code-block:: python

    app = QuickHTML()

3. Define a route for the homepage that returns an `Html` object with a `Div` containing
an `H1` element and a `Button` element:

.. code-block:: python

    @app.route('/')
    async def homepage(request):
        return Html(
                Div(
                    H1('Hello, world!'),
                    Button('Click me', id='button', hx_get='/data'),
                )
            )

4. Define a route for the data endpoint that returns the string "Clicked!":

.. code-block:: python

    @app.route('/data')
    async def data(request):
        return "Clicked!"

5. Start the QuickHTML application using the `serve` method:

.. code-block:: python

    app.serve()

Putting it all together

.. code-block:: python

    from quickhtml import QuickHTML
    from quickhtml.tags import *

    app = QuickHTML()

    @app.route('/')
    async def homepage(request):
        return Html(
                Div(
                    H1('Hello, world!'),
                    Button('Click me', id='button', hx_get='/data'),
                )
            )
        
    @app.route('/data')
    async def data(request):
        return "Clicked!"

    app.serve()

Now you can run the script and visit `http://localhost:8000` in your browser to see
the "Hello, world!" page with a button that updates the page with the response "Clicked!"
when clicked.

Next Steps
----------

Congratulations! You have successfully created a simple QuickHTML application. To learn
more about the features and capabilities of QuickHTML, check out the `Examples` section
of the documentation.