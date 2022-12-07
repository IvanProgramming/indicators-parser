from json import dumps
from urllib.parse import urlparse

from responses.errors import NoGithubCode
from responses.responses import BadResponse
from tests.fixtures.aioresponse import mocked
from tests.fixtures.client import sti


def test_github_oauth(sti, mocked):
    mocked.post("https://github.com/login/oauth/access_token", status=200, body=dumps({
        "access_token": "ghAAAA",
        "scope": "repo,gist",
        "token_type": "bearer"
    }))
    mocked.get("https://api.github.com/user", status=200, body=dumps({"login": "krol", "id": 54}))

    resp = sti.get("/oauth/github?code=12345", follow_redirects=False)

    assert resp.status_code == 301
    assert resp.headers.get("Set-Cookie") == "token=[user=54&login=krol]"


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
