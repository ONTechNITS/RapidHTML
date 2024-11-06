import subprocess
import time
import httpx
import pytest
import os

from rapidhtml.app import RapidHTML, JS_RELOAD_SCRIPT
from rapidhtml.tags import Html, Head, Title

TEST_FILE_HELLO = "live_reload/hello.py"
TEST_FILE_GOODBYE = "live_reload/goodbye.py"
SERVER_FILE = "server.py"


def wait_for_reload(url, expected_json, timeout=10, interval=0.2):
    start_time = time.time()
    while time.time() - start_time < timeout:
        response = httpx.get(url)
        if response.status_code == 200 and response.json() == expected_json:
            return True
        time.sleep(interval)
    return False


@pytest.fixture(scope="module")
def uvicorn_server():
    os.chdir(os.path.dirname(__file__))
    with open(TEST_FILE_HELLO) as f, open(SERVER_FILE, "w") as server_file:
        server_file.write(f.read())
    process = subprocess.Popen(["poetry", "run", "python", SERVER_FILE])
    time.sleep(2)
    yield process
    process.terminate()
    process.wait()
    os.remove(SERVER_FILE)


def test_live_reload(uvicorn_server):
    url = "http://127.0.0.1:8000/"
    assert wait_for_reload(url, {"hello": "world"})
    with open(TEST_FILE_GOODBYE) as f, open(SERVER_FILE, "w") as server_file:
        server_file.write(f.read())
    assert wait_for_reload(url, {"goodbye": "world"})


def test_live_reload_html():
    app = RapidHTML(reload=True)

    html = Html(
        Head(
            Title("RapidHTML Example"),
        ),
    )

    html.add_head(*app.html_head)

    assert JS_RELOAD_SCRIPT in html.render()
