from rapidhtml.app import RapidHTML
from pathlib import Path

app = RapidHTML(
    reload=True,
)


async def homepage(request):
    return {"goodbye": "world"}


app.router.add_routes(
    [
        ("/", homepage),
    ]
)

if __name__ == "__main__":
    app.serve(
        reload_includes=[str(Path(__file__).relative_to(Path(__file__).parent))],
    )
