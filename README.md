# RapidHTML

A PEP8-compliant, well documented and typehinted framework for creating web apps
in a purely Pythonic way. Powered by Javacsript frameworks like HTMX, and with
CSS built-in, write more Python and less of everything else.

## Example

```py
from rapidhtml import RapidHTML
from rapidhtml.tags import *

app = RapidHTML(
    html_head=[Link(rel="stylesheet", href="https://matcha.mizu.sh/matcha.css")]
)

async def clicked_callback():
    return "Clicked!"

@app.route('/')
async def homepage(request):
    return Html(
        Div(
            H1('Hello, world!'),
            Button('Click me', callback=clicked_callback, id='button'),
        )
    )

if __name__ == "__main__":
    app.serve()
```

This will serve the app at http://localhost:8000