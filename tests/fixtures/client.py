import pytest
from starlette.testclient import TestClient
from app import app


@pytest.fixture
def sti() -> TestClient:
    """ Starlette TestClient Instance, wrapped in fixture """
    return TestClient(app)
