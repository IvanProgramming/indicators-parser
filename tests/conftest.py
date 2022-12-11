import asyncio
import os
import pytest
from pytest_asyncio.plugin import SubRequest
from tortoise import Tortoise
from tortoise.contrib.test import finalizer, initializer
from tortoise.exceptions import DBConnectionError, OperationalError

from auth.key import key
from auth.utils import create_and_save_key


@pytest.fixture(scope="session", autouse=True)
def db() -> None:
    config = {
        'connections': {
            'default': "sqlite://test-db.sqlite"
        },
        'apps': {
            'models': {
                'models': ['models'],
                'default_connection': 'default',
            }
        }
    }

    async def _init_db() -> None:
        await Tortoise.init(config)
        try:
            await Tortoise._drop_databases()
        except (DBConnectionError, OperationalError):  # pragma: nocoverage
            pass

        await Tortoise.init(config, _create_db=True)
        await Tortoise.generate_schemas(safe=False)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_init_db())
    yield
    loop = asyncio.new_event_loop()
    loop.run_until_complete(Tortoise._drop_databases())


@pytest.fixture(scope="session", autouse=True)
def load_key():
    create_and_save_key("test_key.jwk")
    key.load_key("test_key.jwk")
    yield
    os.remove("test_key.jwk")
