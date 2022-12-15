import pytest
from integrations.telegram import client


@pytest.fixture()
def telegram():
    client.start()
