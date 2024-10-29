# Getting Started

Welcome to the Getting Started guide for the `RapidHTML` project! This guide will
walk you through the process of creating a simple RapidHTML application.

## Installation

To install RapidHTML, you can use `pip`:

```bash
pip install rapidhtml
```

## Creating a RapidHTML Application

To create a RapidHTML application, you need to create an instance of the `RapidHTML`
class and define routes using the `route` decorator. Here is an example of a simple
RapidHTML application that serves a single page with a button that, when clicked,
sends an AJAX request to the server and updates the page with the response broken down into steps:

1. Import the `RapidHTML` class and the `tags` module:

    ```python
    from rapidhtml import RapidHTML
    from rapidhtml.tags import *
    ```

2. Create an instance of the `RapidHTML` class:

    ```python
    app = RapidHTML()
    ```

3. Define a route for the homepage that returns an `Html` object with a `Div` containing
an `H1` element and a `Button` element:

    ```python
    @app.route('/')
    async def homepage(request):
        return Html(
                Div(
                    H1('Hello, world!'),
                    Button('Click me', id='button', hx_get='/data'),
                )
            )
    ```

4. Define a route for the data endpoint that returns the string "Clicked!":

    ```python
    @app.route('/data')
    async def data(request):
        return "Clicked!"
    ```

5. Start the RapidHTML application using the `serve` method:

    ```python
    app.serve()
    ```

## Putting it all together

```python
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
```

Now you can run the script and visit `http://localhost:8000` in your browser to see
the "Hello, world!" page with a button that updates the page with the response "Clicked!"
when clicked.

## Next Steps

Congratulations! You have successfully created a simple RapidHTML application. To learn
more about the features and capabilities of RapidHTML, check out the `Examples` section
of the documentation.