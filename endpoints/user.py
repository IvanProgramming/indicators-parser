from starlette.requests import Request

from models import User
from models.users import UserPD, BotToken
from responses.errors import BotTokenDontExist
from responses.responses import OkResponse


async def get_me(request: Request):
    """ Returns user itself serialized """
    user: User = request.state.user
    user_model = UserPD.from_orm(user)
    return OkResponse(user_model)


async def create_bot_token(request: Request):
    """ Creates and returns bot token """
    user: User = request.state.user
    expires = int(request.query_params.get("expires", 1))
    token = user.create_token(for_bot=True)
    await BotToken.create_from_token(token, expires)
    return OkResponse({"token": token})


async def get_bot_tokens(request: Request):
    """ Returns all bot tokens of user """
    user: User = request.state.user
    tokens = await BotToken.filter(user=user).all()
    return OkResponse({"tokens": [{"id": str(token.id)[:4], "expires_in": token.expires_at} for token in tokens]})


async def delete_bot_token(request: Request):
    """ Deletes bot token """
    user: User = request.state.user
    token_id = request.query_params["token_id"]
    token = await BotToken.get_or_none(id=token_id)
    if token is None:
        raise BotTokenDontExist
    return OkResponse({"deleted": await token.delete()})
