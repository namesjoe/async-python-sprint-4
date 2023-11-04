from fastapi.testclient import TestClient

# Import the app fixture from conftest
from .conftest import app


# Your test functions
def test_read_root(test_client: TestClient):
    response = test_client.get(app.url_path_for("read_root"))
    assert response.status_code == 200
    assert response.json() == {"message": "Short link here!"}


def test_shorten_url_without_authentication(test_client: TestClient):
    response = test_client.post(app.url_path_for("shorten"),
                                json={"url": "http://google.com"})
    assert response.status_code == 401
