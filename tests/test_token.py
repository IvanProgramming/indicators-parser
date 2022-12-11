import pytest

from auth.middleware import parse_token
from responses.errors import TokenUndefinedError
from tests.fixtures.client import sti
from models.users import User
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
