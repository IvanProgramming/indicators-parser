from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from auth.key import decrypt_token
from models import User
from responses.errors import TokenUndefinedError, UserDontExist


def parse_token(request: Request) -> str:
    """ Parses token from http request

    Args:
        request: Starlette request object
    Raises:
        TokenUndefinedError if token is not presented with Token keyword
    """
    token_header = request.headers.get("Authorization")
    if token_header is not None and token_header.startswith("Token "):
        if token_header[6:].strip() != "":
            return token_header[6:].strip()
    raise TokenUndefinedError


class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    """ JWT Authentication middleware """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        token = parse_token(request)
        data = decrypt_token(token)
        user = await User.get_or_none(id=data["user_id"])
        if user is None:
            raise UserDontExist
        request.state.token_data = data
        request.state.user = user
        return await call_next(request)

