import pytest
from requests import get

from models.indicator import IndicatorGroup, Indicator, IndicatorType
from parsers.text_parser import CollectedData
from responses.errors import ReportNotPresented
from tests.fixtures.tortoise import user
from tests.fixtures.client import sti_auth


@pytest.mark.asyncio
async def test_indicator_group_from_reports_collected_data(user):
    data = CollectedData(
        hashes={"5d41402abc4b2a76b9719d911017c592"},
        ips={"100.100.100.100"},
        urls={"https://www.google.com/"}
    )
    group = await IndicatorGroup.from_reports_collected_data(data, user)

    indicators = await Indicator.filter(group=group).all()

    assert len(indicators) == 3
    for indicator in indicators:
        if indicator.type == IndicatorType.HASH:
            assert indicator.value == "5d41402abc4b2a76b9719d911017c592"
        elif indicator.type == IndicatorType.IP_ADDRESS:
            assert indicator.value == "100.100.100.100"
        elif indicator.type == IndicatorType.URL:
            assert indicator.value == "https://www.google.com/"


@pytest.mark.asyncio
async def test_load_pdf_endpoint(user, sti_auth):
    pdf_url = "https://storage.yandexcloud.net/ivanprogramming/Network_Report.pdf"
    pdf_path = "Network_Report.pdf"
    with open(pdf_path, "wb") as f:
        f.write(get(pdf_url).content)

    resp = sti_auth.post("/api/loadReport", files={"file": open(pdf_path, "rb")})
    assert resp.status_code == 200
    data = resp.json()["data"]

    group_id = data["group"]["id"]
    group = await IndicatorGroup.get(id=group_id)
    count_of_indicators = await Indicator.filter(group=group).count()

    assert count_of_indicators == 20


def test_load_pdf_endpoint_no_file(sti_auth):
    resp = sti_auth.post("/api/loadReport", files={})

    assert resp.status_code == 422
    assert not resp.json()["ok"]
    assert resp.json()["data"]["error_code"] == ReportNotPresented.code
