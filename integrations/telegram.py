from telethon import TelegramClient, events
from telethon.tl.custom import Message

from parsers.text_parser import find_ioc, CollectedData
from settings import TELEGRAM_SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH

api_id = TELEGRAM_API_ID
api_hash = TELEGRAM_API_HASH

client = TelegramClient(TELEGRAM_SESSION_NAME, api_id, api_hash)


@client.on(events.NewMessage(incoming=True))
async def on_message(event: Message):
    from models import TelegramWatcher, Indicator
    if event.is_channel:
        entity = await client.get_entity(event.chat_id)
        watchers = await TelegramWatcher.filter(chat_id=entity.id).all()
        if len(watchers) > 0:
            if event.message.message is not None:
                message_indicators: CollectedData = find_ioc(event.message.message)
                created_indicators = []
                for watcher in watchers:
                    created_indicators += message_indicators.indicators(group_id=watcher.indicator_group_id,
                                                                        owner_id=watcher.owner_id)
                if len(created_indicators) > 0:
                    await Indicator.bulk_create(created_indicators)
