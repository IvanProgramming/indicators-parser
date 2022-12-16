from json import dumps
from urllib.parse import urlparse

import pytest

from auth.key import decrypt_token, key
from auth.utils import create_and_save_key
from models import User
from responses.errors import NoGithubCode
from tests.fixtures.aioresponse import mocked
from tests.fixtures.client import sti


@pytest.mark.asyncio
async def test_github_oauth(sti, mocked):
    mocked.post("https://github.com/login/oauth/access_token", status=200, body=dumps({
        "access_token": "ghAAAA",
        "scope": "repo,gist",
        "token_type": "bearer"
    }))
    mocked.get("https://api.github.com/user", status=200, body=dumps({"login": "krol", "id": 54}))

    resp = sti.get("/oauth/github?code=12345", follow_redirects=False)

    assert resp.status_code == 301
    token = resp.cookies.get("token")
    claims = decrypt_token(token)
    uid = claims["user_id"]

    user = await User.get(id=uid)
    assert user.github_user_id == 54


def test_github_oauth_no_code(sti):
    resp = sti.get("/oauth/github")

    assert resp.status_code == 422
    assert resp.json()["data"]["error_code"] == NoGithubCode().code


def test_github_oauth_redirect(sti):
    resp = sti.get("/login/github", follow_redirects=False)

    assert resp.status_code == 301
    redirect_url = urlparse(resp.headers["Location"])
    assert redirect_url.path == "/login/oauth/authorize"
    assert redirect_url.hostname == "github.com"


def test_login_redirect_token_page(mocked, sti):
    mocked.post("https://github.com/login/oauth/access_token", status=200, body=dumps({
        "access_token": "ghAAAA",
        "scope": "repo,gist",
        "token_type": "bearer"
    }))
    mocked.get("https://api.github.com/user", status=200, body=dumps({"login": "krol", "id": 54}))
    resp = sti.get("/oauth/github?code=12345")

    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "text/html; charset=utf-8"
