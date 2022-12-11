import pytest
from tortoise import Tortoise
from tortoise.contrib.test import finalizer
from asyncio import get_event_loop

from models import User
from models.users import UserPD


@pytest.fixture()
def remove_db_on_end():
    yield
    loop = get_event_loop()
    loop.run_until_complete(Tortoise._drop_databases())


@pytest.fixture()
def user():
    user = User(
        id=777,
        github_user_id=1,
    )
    user.github_username = "krol"
    user_pd = UserPD.from_orm(user)
    print(user_pd.json())
    loop = get_event_loop()
    loop.run_until_complete(user.save())
    return user
