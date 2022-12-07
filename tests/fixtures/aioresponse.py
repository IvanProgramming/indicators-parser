import asyncio

import pytest
from aioresponses import aioresponses


# Example from https://github.com/pnuckowski/aioresponses
@pytest.fixture
def mocked():
    with aioresponses() as m:
        yield m


# Example from https://github.com/pnuckowski/aioresponses

@pytest.fixture
def async_loop():
    return asyncio.get_event_loop()
