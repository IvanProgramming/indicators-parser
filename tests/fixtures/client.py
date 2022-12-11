import pytest
from starlette.testclient import TestClient

from app import app


@pytest.fixture
def sti() -> TestClient:
    """ Starlette TestClient Instance, wrapped in fixture """
    return TestClient(app)


@pytest.fixture
def sti_auth(user) -> TestClient:
    """ Starlette TestClient, authenticated as TestUser """
    token = user.create_token()
    test_client = TestClient(app)
    test_client.headers = {
        "Authorization": f"Token {token}"
    }
    return test_client
