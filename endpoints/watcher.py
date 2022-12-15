from starlette.requests import Request

from models import TelegramWatcher
from models.watcher import TelegramWatcherPD
from responses.errors import TelegramInvalidLink
from responses.responses import OkResponse


async def create_watcher(request: Request):
    """ Creates TelegramWatcher from telegram channel invite link """
    chat_invite_link = (await request.json())["chat_invite_link"]
    if not chat_invite_link:
        raise TelegramInvalidLink

    watcher = await TelegramWatcher.from_telegram_link(chat_invite_link, request.state.user)
    return OkResponse({"watcher": TelegramWatcherPD.from_orm(watcher)})
