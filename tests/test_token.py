import pytest

from auth.middleware import parse_token
from responses.errors import TokenUndefinedError, BotTokenDontExist
from tests.fixtures.client import sti, sti_auth
from tests.fixtures.tortoise import user
from models.users import User, BotToken
from auth.utils import create_and_save_key
from auth.key import key, decrypt_token


def test_token_generation():
    create_and_save_key("key.jwk")
    key.load_key("key.jwk")

    user = User(id=54, github_user_id=100, github_username="krol")
    token = user.create_token()

    claims = decrypt_token(token)

    assert claims["user_id"] == 54


def test_parse_token(sti):
    request = sti.build_request("GET", "/some-url", headers={
        "Authorization": "Token S0m3T0k3n"
    })

    token = parse_token(request)
    assert token == "S0m3T0k3n"


def test_parse_token_no_token(sti):
    request = sti.build_request("GET", "/some-url")

    with pytest.raises(TokenUndefinedError):
        parse_token(request)


def test_parse_token_just_header(sti):
    request = sti.build_request("GET", "/some-url", headers={
        "Authorization": "Token"
    })

    with pytest.raises(TokenUndefinedError):
        parse_token(request)


@pytest.mark.asyncio
async def test_create_bot_token(user):
    token = user.create_token(for_bot=True)
    await BotToken.create_from_token(token)

    bot_token = await BotToken.get(user=user)
    claims = decrypt_token(token)
    assert claims["bot_token_id"] == str(bot_token.id)


def test_bot_token_create_endpoint(sti_auth, sti, user):
    response = sti_auth.get("/api/createBotToken")
    assert response.status_code == 200
    assert response.json()["data"]["token"] is not None

    response = sti.get("/api/getMe", headers={
        "Authorization": f"Token {response.json()['data']['token']}"
    })

    assert response.status_code == 200
    assert response.json()['data']["id"] == user.id


def test_bot_token_create_and_delete(sti_auth, sti):
    response = sti_auth.get("/api/createBotToken")
    token = response.json()["data"]["token"]
    token_id = decrypt_token(token)["bot_token_id"]
    resp = sti_auth.get(f"/api/deleteBotToken?token_id={token_id}")
    assert resp.status_code == 200

    incorrect_response = sti.get("/api/getMe", headers={
        "Authorization": f"Token {token}"
    })
    assert incorrect_response.status_code == 404
    assert incorrect_response.json()["data"]["error_code"] == BotTokenDontExist.code


def test_bot_token_create_many_and_get(sti_auth):
    for _ in range(5):
        response = sti_auth.get("/api/createBotToken")
        assert response.status_code == 200
        assert response.json()["data"]["token"] is not None

    response = sti_auth.get("/api/getBotTokens")
    assert response.status_code == 200
    assert len(response.json()["data"]["tokens"]) == 5
