import asyncio
import os

import pytest
from requests import get

from models import IndicatorGroup
from parsers.text_parser import CollectedData
from tests.fixtures.tortoise import user


@pytest.fixture
def mts_report():
    pdf_url = "https://storage.yandexcloud.net/ivanprogramming/Network_Report.pdf"
    pdf_path = "Network_Report.pdf"
    with open(pdf_path, "wb") as f:
        f.write(get(pdf_url).content)
    yield pdf_path
    try:
        os.remove(pdf_path)
    except FileNotFoundError:
        pass


@pytest.fixture
def group(user):
    async def _create_group():
        collected_data = CollectedData(
            hashes={"5d41402abc4b2a76b9719d911017c592"},
            ips={"101.100.100.100"},
            urls={"https://www.google.com/"}
        )
        group = await IndicatorGroup.from_reports_collected_data(collected_data, user)
        return group

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_create_group())
