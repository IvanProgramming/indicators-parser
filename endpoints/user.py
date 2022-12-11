from starlette.requests import Request

from models import User
from models.users import UserPD
from responses.responses import OkResponse


async def get_me(request: Request):
    """ Returns user itself serialized """
    user: User = request.state.user
    print(user)
    user_model = UserPD.from_orm(user)
    return OkResponse(user_model)
