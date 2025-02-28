from uuid import uuid4

import pytest
from requests import get

from models.indicator import IndicatorGroup, Indicator, IndicatorType
from parsers.text_parser import CollectedData
from responses.errors import ReportNotPresented, IndicatorGroupDoesNotExist, ReportNotFound
from tests.fixtures.tortoise import user
from tests.fixtures.client import sti_auth
from tests.fixtures.indicators import mts_report
from tests.fixtures.indicators import group
from random import randint


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
async def test_load_pdf_endpoint(user, sti_auth, mts_report):
    resp = sti_auth.post("/api/loadReport", files={"file": open(mts_report, "rb")})
    assert resp.status_code == 200
    data = resp.json()["data"]

    group_id = data["indicator_group"]["id"]
    group = await IndicatorGroup.get(id=group_id)
    count_of_indicators = await Indicator.filter(group=group).count()

    assert count_of_indicators == 20


def test_load_pdf_endpoint_no_file(sti_auth):
    resp = sti_auth.post("/api/loadReport", files={})

    assert resp.status_code == 422
    assert not resp.json()["ok"]
    assert resp.json()["data"]["error_code"] == ReportNotPresented.code


def test_indicator_endpoint_not_found(sti_auth, group):
    resp = sti_auth.get("/api/getIndicatorsFromGroup?group_id=not-exists")

    assert resp.status_code == 404
    assert not resp.json()["ok"]
    assert resp.json()["data"]["error_code"] == IndicatorGroupDoesNotExist.code


def test_indicator_endpoint(sti_auth, group):
    resp = sti_auth.get(f"/api/getIndicatorsFromGroup?group_id={group.id}")

    assert resp.status_code == 200

    assert len(resp.json()["data"]["indicators"]) == 3


def test_indicator_endpoint_pagination(sti_auth, group):
    resp = sti_auth.get(f"/api/getIndicatorsFromGroup?group_id={group.id}&page=2")

    assert resp.status_code == 200

    assert len(resp.json()["data"]["indicators"]) == 0


@pytest.mark.asyncio
async def test_indicator_groups_endpoint(sti_auth, user):
    groups_count = randint(5, 12)
    groups = []
    for _ in range(groups_count):
        groups.append(IndicatorGroup(
            id=str(uuid4()),
            owner=user,
            description="Test group"
        ))
    await IndicatorGroup.bulk_create(groups)

    resp = sti_auth.get("/api/getIndicatorGroups")

    assert resp.status_code == 200
    assert len(resp.json()["data"]) == len(groups)


def test_reports_endpoint(sti_auth, user, mts_report):
    resp = sti_auth.post("/api/loadReport", files={"file": open(mts_report, "rb")})

    assert resp.status_code == 200
    report_id = resp.json()["data"]["report_id"]

    resp_reports = sti_auth.get("/api/getReports")
    assert 1 == len(resp_reports.json()["data"])
    print(resp_reports.json())
    assert resp_reports.json()["data"][0]["id"] == report_id


def test_parse_link_report_empty(sti_auth):
    test_url = "https://storage.yandexcloud.net/ivanprogramming/empty_report.html"

    resp = sti_auth.get(f"/api/loadPageReport?url={test_url}")
    assert resp.status_code == 200

    data = resp.json()["data"]
    report_id = data["indicator_group"]["id"]

    resp = sti_auth.get(f"/api/getIndicatorsFromGroup?group_id={report_id}")
    assert resp.status_code == 200

    assert len(resp.json()["data"]["indicators"]) == 0


def test_parse_link_report(sti_auth):
    test_url = "https://storage.yandexcloud.net/ivanprogramming/report.html"

    resp = sti_auth.get(f"/api/loadPageReport?url={test_url}")
    assert resp.status_code == 200

    data = resp.json()["data"]
    report_id = data["indicator_group"]["id"]

    resp = sti_auth.get(f"/api/getIndicatorsFromGroup?group_id={report_id}")
    assert resp.status_code == 200

    assert len(resp.json()["data"]["indicators"]) == 3


def test_report_link_generation(sti_auth, mts_report):
    resp = sti_auth.post("/api/loadReport", files={"file": open(mts_report, "rb")})

    assert resp.status_code == 200
    report_id = resp.json()["data"]["report_id"]

    resp = sti_auth.get(f"/api/getReportFilePath?report_id={report_id}")
    assert resp.status_code == 200
    link = resp.json()["data"]["link"]

    print(link)

    resp = get(link)
    assert resp.status_code == 200


def test_report_link_generation_not_found(sti_auth):
    resp = sti_auth.get(f"/api/getReportFilePath?report_id=not-exists")
    assert resp.status_code == 404
    assert not resp.json()["ok"]
    assert resp.json()["data"]["error_code"] == ReportNotFound.code
