import pytest
from tortoise import Tortoise
from asyncio import get_event_loop

from models import User


@pytest.fixture()
def user():
    user = User(
        id=777,
        github_user_id=1,
        github_username="krol"
    )
    loop = get_event_loop()
    loop.run_until_complete(user.save())
    return user
