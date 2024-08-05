Hello World 
===========

The simplest example of a QuickHTML application is a simple "Hello, world!" page.
This example demonstrates how to create a basic QuickHTML application that serves 
a single page with a button that, when clicked, sends an AJAX request to the 
server and updates the page with the response.

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