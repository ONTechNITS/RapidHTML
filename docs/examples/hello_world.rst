Hello World 
===========

The simplest example of a RapidHTML application is a simple "Hello, world!" page.
This example demonstrates how to create a basic RapidHTML application that serves 
a single page with a button that, when clicked, sends an AJAX request to the 
server and updates the page with the response.

.. code-block:: python

    from rapidhtml import RapidHTML
    from rapidhtml.tags import *

    app = RapidHTML()

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