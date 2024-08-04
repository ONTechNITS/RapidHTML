# QuickHTML

A project for developing web apps totally in Python

## Example

```py
from quickhtml import QuickHTML
from quickhtml.tags import *

app = QuickHTML(
    html_head=[Link(rel="stylesheet", href="https://matcha.mizu.sh/matcha.css")]
)

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

app.serve(port=8001)
```

This will serve the app at http://localhost:8000