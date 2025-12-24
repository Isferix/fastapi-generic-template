import contextlib
import threading
import time

# import pytest
import uvicorn
from fastapi.testclient import TestClient
from ..main import server


class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


client = TestClient(server)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# @pytest.fixture(scope="session")
# def test_live_server():
#     config = uvicorn.Config(
#         "main:server", host="127.0.0.1", port=5000, log_level="info"
#     )
#     live_server = Server(config=config)
#     with live_server.run_in_thread():
#         yield
