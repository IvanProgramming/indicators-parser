from os import getenv

from models import IndicatorGroup, Indicator
from models.watcher import TelegramWatcher
from tests.fixtures.telegram import telegram
from tests.fixtures.tortoise import user
from integrations.telegram import on_message
from telethon.tl.custom import Message
import pytest


@pytest.mark.skipif(getenv("SKIP_TELEGRAM_TESTS"), reason="Telegram tests are skipped")
@pytest.mark.asyncio
async def test_watcher(telegram, user):
    await TelegramWatcher.from_telegram_link("https://t.me/+xkMQwHvx2wsyMDEy", user)

    indicator_groups = await IndicatorGroup.filter(owner=user).count()
    assert indicator_groups == 1


@pytest.mark.skip()
@pytest.mark.asyncio
async def test_watcher_message(telegram, user):
    watcher = await TelegramWatcher.from_telegram_link("https://t.me/+xkMQwHvx2wsyMDEy", user)

    message = Message(
        message="Hash: 098890dde069e9abad63f19a0d9e1f32, Url: https://google.com",
        id=4,
        peer_id=1749453629
    )

    await on_message(message)

    assert (await Indicator.filter(indicator_group_id=watcher.indicator_group_id).count()) == 2
