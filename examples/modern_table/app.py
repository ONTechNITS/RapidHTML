from rapidhtml import RapidHTML
from rapidhtml.tags import Html, Head, Style, Body

from table_html import load_database, generate_html
from styles import table_styling

app = RapidHTML()

CACHED_RESPONSE = None


def get_html_response() -> Html:
    return Html(Head(Style(table_styling)), Body(generate_html(*load_database())))


@app.route("/")
async def serve_table():
    global CACHED_RESPONSE

    if CACHED_RESPONSE is not None:
        return CACHED_RESPONSE

    CACHED_RESPONSE = get_html_response()

    return CACHED_RESPONSE


if __name__ == "__main__":
    CACHED_RESPONSE = get_html_response()
    app.serve()
