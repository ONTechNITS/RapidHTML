from starlette.testclient import TestClient
from starlette.websockets import WebSocket  # Added import
from quickhtml.routing import QuickHTMLWSEndpoint
from quickhtml import QuickHTML


def test_ws():
    test_app = QuickHTML()

    class Echo(QuickHTMLWSEndpoint):
        encoding = "text"

        async def on_connect(self, websocket):
            await websocket.accept()
            await websocket.send_text("test")

    test_app.router.add_websocket_route("/ws", Echo)

    client = TestClient(test_app)

    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_text()
        assert data == "test"


def test_ws_receive():
    test_app = QuickHTML()

    class Echo(QuickHTMLWSEndpoint):
        encoding = "text"

        async def on_connect(self, websocket):
            await websocket.accept()
            await websocket.send_text("connected")

        async def on_receive(self, websocket, data):
            await websocket.send_text(f"Echo: {data}")

    test_app.router.add_websocket_route("/ws", Echo)

    client = TestClient(test_app)

    with client.websocket_connect("/ws") as websocket:
        initial_message = websocket.receive_text()
        assert initial_message == "connected"

        websocket.send_text("Hello, Echo!")
        response = websocket.receive_text()
        assert response == "Echo: Hello, Echo!"


def test_ws_different_encodings():
    test_app = QuickHTML()

    class Echo(QuickHTMLWSEndpoint):
        encoding = "bytes"

        async def on_connect(self, websocket):
            await websocket.accept()
            await websocket.send_bytes(b"test bytes")

    test_app.router.add_websocket_route("/ws", Echo)

    client = TestClient(test_app)

    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_bytes()
        assert data == b"test bytes"


def test_ws_different_message_types():
    test_app = QuickHTML()

    class Echo(QuickHTMLWSEndpoint):
        encoding = "json"

        async def on_connect(self, websocket):
            await websocket.accept()
            await websocket.send_json({"message": "test json"})

    test_app.router.add_websocket_route("/ws", Echo)

    client = TestClient(test_app)

    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert data == {"message": "test json"}


def test_ws_close_code():
    test_app = QuickHTML()
    close_code_received = None

    class Echo(QuickHTMLWSEndpoint):
        encoding = "text"

        async def on_connect(self, websocket):
            await websocket.accept()

        async def on_disconnect(self, websocket, close_code):
            nonlocal close_code_received
            close_code_received = close_code

    test_app.router.add_websocket_route("/ws", Echo)

    client = TestClient(test_app)

    with client.websocket_connect("/ws") as websocket:
        websocket.close(code=1000)

    assert close_code_received == 1000


def test_ws_multiple_connections():
    test_app = QuickHTML()

    class Echo(QuickHTMLWSEndpoint):
        encoding = "text"

        async def on_connect(self, websocket):
            await websocket.accept()
            await websocket.send_text("connected")

    test_app.router.add_websocket_route("/ws", Echo)

    client = TestClient(test_app)

    with client.websocket_connect("/ws") as websocket1, client.websocket_connect(
        "/ws"
    ) as websocket2:
        message1 = websocket1.receive_text()
        message2 = websocket2.receive_text()
        assert message1 == "connected"
        assert message2 == "connected"


def test_ws_with_decorator():
    app = QuickHTML()

    @app.websocket_route("/ws")
    class Echo(QuickHTMLWSEndpoint):
        encoding = "text"

        async def on_connect(self, websocket: WebSocket):
            await websocket.accept()
            await websocket.send_text("Hello, world!")

        async def on_receive(self, websocket: WebSocket, data: str):
            pass

        async def on_disconnect(self, websocket: WebSocket, close_code: int):
            pass

    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_text()
        assert data == "Hello, world!"


def test_ws_receive_with_decorator():
    app = QuickHTML()

    @app.websocket_route("/ws")
    class Echo(QuickHTMLWSEndpoint):
        encoding = "text"

        async def on_connect(self, websocket: WebSocket):
            await websocket.accept()
            await websocket.send_text("connected")

        async def on_receive(self, websocket: WebSocket, data: str):
            await websocket.send_text(f"Echo: {data}")

    client = TestClient(app)

    with client.websocket_connect("/ws") as websocket:
        initial_message = websocket.receive_text()
        assert initial_message == "connected"

        websocket.send_text("Hello, Echo!")
        response = websocket.receive_text()
        assert response == "Echo: Hello, Echo!"


def test_ws_different_encodings_with_decorator():
    app = QuickHTML()

    @app.websocket_route("/ws")
    class Echo(QuickHTMLWSEndpoint):
        encoding = "bytes"

        async def on_connect(self, websocket: WebSocket):
            await websocket.accept()
            await websocket.send_bytes(b"test bytes")

    client = TestClient(app)

    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_bytes()
        assert data == b"test bytes"


def test_ws_different_message_types_with_decorator():
    app = QuickHTML()

    @app.websocket_route("/ws")
    class Echo(QuickHTMLWSEndpoint):
        encoding = "json"

        async def on_connect(self, websocket: WebSocket):
            await websocket.accept()
            await websocket.send_json({"message": "test json"})

    client = TestClient(app)

    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert data == {"message": "test json"}


def test_ws_close_code_with_decorator():
    app = QuickHTML()
    close_code_received = None

    @app.websocket_route("/ws")
    class Echo(QuickHTMLWSEndpoint):
        encoding = "text"

        async def on_connect(self, websocket: WebSocket):
            await websocket.accept()

        async def on_disconnect(self, websocket: WebSocket, close_code: int):
            nonlocal close_code_received
            close_code_received = close_code

    client = TestClient(app)

    with client.websocket_connect("/ws") as websocket:
        websocket.close(code=1000)

    assert close_code_received == 1000


def test_ws_multiple_connections_with_decorator():
    app = QuickHTML()

    @app.websocket_route("/ws")
    class Echo(QuickHTMLWSEndpoint):
        encoding = "text"

        async def on_connect(self, websocket: WebSocket):
            await websocket.accept()
            await websocket.send_text("connected")

    client = TestClient(app)

    with client.websocket_connect("/ws") as websocket1, client.websocket_connect(
        "/ws"
    ) as websocket2:
        message1 = websocket1.receive_text()
        message2 = websocket2.receive_text()
        assert message1 == "connected"
        assert message2 == "connected"
