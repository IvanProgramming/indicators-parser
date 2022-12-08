from json import loads
from os import remove

import httpx as httpx
from auth.utils import create_and_save_key
from jwcrypto.jwk import JWK
from tests.fixtures.client import sti


def test_ping(sti):
    resp: httpx.Response = sti.get("/ping")
    print(resp.text)
    data = resp.json()
    assert data == {"ok": True, "data": {}}


def test_key_generation():
    create_and_save_key("test_key.jwk")

    with open("test_key.jwk") as f:
        key = JWK(**loads(f.read()))

    remove("test_key.jwk")
