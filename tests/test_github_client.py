from json import dumps

import pytest

from integrations.github import GithubAPI
from responses.errors import GithubBadCodeError, GithubError
from tests.fixtures.aioresponse import mocked, async_loop


def test_github_process_code_success(mocked, async_loop):
    mocked.post("https://github.com/login/oauth/access_token", status=200,
                body=dumps({"access_token": "ghAAA", "scope": "repo,gist", "token_type": "bearer"}))
    token = async_loop.run_until_complete(GithubAPI.process_code("s0mec0de"))

    assert token == "ghAAA"


def test_github_process_code_bad_code(mocked, async_loop):
    mocked.post("https://github.com/login/oauth/access_token", status=200,
                body=dumps(
                    {"error": "bad_verification_code", "error_description": "The code passed is incorrect or expired.",
                     "error_uri": "https://youtu.be/dQw4w9WgXcQ"}))

    with pytest.raises(GithubBadCodeError):
        token = async_loop.run_until_complete(GithubAPI.process_code("s0mec0de"))


def test_github_process_code_gh_error(mocked, async_loop):
    mocked.post("https://github.com/login/oauth/access_token", status=200,
                body=dumps({"error": "incorrect_client_credentials",
                            "error_description": "The client_id and/or client_secret passed are incorrect.",
                            "error_uri": "https://youtu.be/dQw4w9WgXcQ"}))
    with pytest.raises(GithubError):
        token = async_loop.run_until_complete(GithubAPI.process_code("s0mec0de"))

    mocked.post("https://github.com/login/oauth/access_token", status=404,
                body=dumps({"custom": "not_found"}))
    with pytest.raises(GithubError):
        token = async_loop.run_until_complete(GithubAPI.process_code("s0mec0de"))


def test_github_user_ok(mocked, async_loop):
    mocked.get("https://api.github.com/user", status=200, body=dumps({"login": "krol", "id": 54}))
    gh_data = async_loop.run_until_complete(GithubAPI.get_user("access_token"))

    assert gh_data == {"user_id": 54, "username": "krol"}


def test_github_user_bad(mocked, async_loop):
    mocked.get("https://api.github.com/user", status=401, body=dumps({"error": "unauthorized"}))

    with pytest.raises(GithubError):
        gh_data = async_loop.run_until_complete(GithubAPI.get_user("access_token"))
