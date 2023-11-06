from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest

from .conftest import app


@pytest.mark.asyncio
async def test_read_root(test_client: TestClient):
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.get(app.url_path_for("read_root"))
        assert response.status_code == 200
        assert response.json() == {"message": "Short link here!"}

@pytest.mark.asyncio
async def test_shorten_url_without_authentication(test_client: TestClient):
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post(app.url_path_for("shorten"), json={"url": "http://google.com"})
        assert response.status_code == 401
