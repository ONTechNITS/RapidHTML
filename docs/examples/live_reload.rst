Live Reload
===========

The Live Reload feature allows your web application to automatically reload the page when the server detects changes in the code. This is particularly useful during development, enabling you to see updates in real-time without the need to manually refresh the page.

To enable Live Reload, you can modify the hello world example by adding the reload flag to your app initialization.


.. important::
    Live reloading requires the app.serve invocation to be within the main block. This is because we're using uvicorn.run() to start the server, and the reload feature in Uvicorn will not simply re-un the script when it detects a change in the code, it will re-load the file as if it were a library, which will cause the app.serve to be called again, causing a conflict. With a main block, this is avoided. In the future we hope to remove this limitation.

.. code-block:: python

    from rapidhtml import RapidHTML
    from rapidhtml.tags import *

    app = RapidHTML(reload=True)

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

    if __name__ == '__main__':
        app.serve()

When you run the server with the reload flag set to True, the server will automatically reload the page when it detects a code change. This allows you to see changes in real-time without manually refreshing the page. This is done by injecting a script into the page that connects to a socket at /live-reload. When the server reloads due to a change, this script triggers a webpage reload on the disconnect event and attempts to connect to the same socket at /live-reload.