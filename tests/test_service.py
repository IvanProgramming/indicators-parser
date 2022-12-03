import httpx as httpx
from tests.fixtures.client import sti


def test_ping(sti):
    resp: httpx.Response = sti.get("/ping")
    print(resp.text)
    data = resp.json()
    assert data == {"ok": True, "data": {}}
