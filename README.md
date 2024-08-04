# QuickHTML

A project for developing web apps totally in Python

## Example

```py
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
```

This will serve the app at http://localhost:8000