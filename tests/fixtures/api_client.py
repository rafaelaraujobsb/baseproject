import pytest
from fastapi.testclient import TestClient

from src.api import start_api


@pytest.fixture(scope="module")
def test_client():
    app = start_api(version="test")

    client = TestClient(app)

    yield client
