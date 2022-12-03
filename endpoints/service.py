from starlette.requests import Request

from responses.responses import OkResponse


async def ping(request: Request) -> OkResponse:
    """ Just ping endpoint. Get method, returns ok """
    return OkResponse({})
