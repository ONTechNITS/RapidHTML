import subprocess
import time
import httpx
import pytest
import os

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
    os.chdir(
        os.path.dirname(__file__)
    )  # Ensure the working directory is the tests directory
    with open(TEST_FILE_HELLO) as f, open(SERVER_FILE, "w") as server_file:
        server_file.write(f.read())

    process = subprocess.Popen(["poetry", "run", "python", SERVER_FILE])
    time.sleep(2)
    yield process
    process.terminate()
    process.wait()
    os.remove(SERVER_FILE)


def test_live_reload(uvicorn_server):
    url = "http://127.0.0.1:8005/"

    # Initial check
    assert wait_for_reload(url, {"hello": "world"})

    # Swap files
    with open(TEST_FILE_GOODBYE) as f, open(SERVER_FILE, "w") as server_file:
        server_file.write(f.read())

    # Check for reload
    assert wait_for_reload(url, {"goodbye": "world"})
