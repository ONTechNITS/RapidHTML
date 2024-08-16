# RapidHTML

A project for developing web apps totally in Python

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