import uuid
from urllib.parse import urlparse
from uuid import uuid4

from pydantic import BaseModel
from telethon.tl.functions.messages import ImportChatInviteRequest, CheckChatInviteRequest
from telethon.tl.types import ChatInviteAlready
from tortoise import Model, fields

from integrations.telegram import client
from models import User, IndicatorGroup
from models.indicator import IndicatorGroupPD
from models.users import UserPD
from responses.errors import TelegramInvalidLink


class TelegramWatcher(Model):
    """ TelegramWatcher ORM object """
    id = fields.UUIDField(pk=True)
    chat_id = fields.IntField()
    owner = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE)
    indicator_group = fields.ForeignKeyField('models.IndicatorGroup', on_delete=fields.CASCADE)

    @staticmethod
    async def from_telegram_link(link: str, owner: User):
        """ Creates TelegramWatcher from link """
        parse_url = urlparse(link)
        if parse_url.scheme != "https" or parse_url.netloc != "t.me":
            raise TelegramInvalidLink
        path = parse_url.path
        if path.startswith("/+"):
            invite = path[2:]
            channel = await client(CheckChatInviteRequest(invite))
            if type(channel) is not ChatInviteAlready:
                updates = await client(ImportChatInviteRequest(invite))
                channel = updates.chats[0]
                channel_id = channel.id
            else:
                channel_id = channel.chat.id
        elif path.startswith("/@"):
            channel_username = path[2:]
            channel = await client.get_entity(channel_username)
            channel_id = channel.id
        else:
            raise TelegramInvalidLink
        indicator_group = IndicatorGroup(
            id=str(uuid4()),
            owner=owner,
            description=f"from telegram channel {channel_id}",
        )
        await indicator_group.save()
        watcher = TelegramWatcher(
            id=str(uuid4()),
            chat_id=channel_id,
            owner=owner,
            indicator_group=indicator_group,
        )
        await watcher.save()
        return watcher


class TelegramWatcherPD(BaseModel):
    """ TelegramWatcher Pydantic object """

    id: uuid.UUID
    """ Unique ID of TelegramWatcher """
    chat_id: int
    """ Telegram chat ID """
    owner: UserPD
    """ Owner of TelegramWatcher """
    indicator_group: IndicatorGroupPD
    """ Indicator group that used to save indicators """

    class Config:
        orm_mode = True
