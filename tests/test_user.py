import httpx
import pytest

from models import User
from tests.fixtures.client import sti_auth


def test_account_get(sti_auth):
    resp: httpx.Response = sti_auth.get("/api/getMe")
    assert resp.status_code == 200
    assert resp.json()["data"]["id"] == 777


@pytest.mark.asyncio
async def test_id_generation(user):
    uid = await User.generate_id()
    assert uid == 778


@pytest.mark.asyncio
async def test_id_generation_no_user():
    uid = await User.generate_id()
    assert uid == 1
