from starlette.requests import Request

from responses.responses import BadResponse


class ApiError(Exception):
    """ Base API error """
    code: int
    description: str
    http_code: int = 500

    def as_response(self):
        """ Error as a response """
        return BadResponse(self.code, self.description, self.http_code)


async def handle_api_error(req: Request, exc: ApiError):
    """ ApiError default starlette handler """
    return exc.as_response()


class GithubBadCodeError(ApiError):
    """ GitHub callback code error """
    code = 101
    description = "Github authorization code is incorrect"
    http_code = 422


class GithubError(ApiError):
    """ GitHub internal bad response """
    code = 102
    description = "Github authorization error"
    http_code = 500


class NoGithubCode(ApiError):
    """ No GitHub auth code provided """
    code = 103
    description = "Github code not provided"
    http_code = 422


class TokenUndefinedError(ApiError):
    """ No token provided in auth-required request """
    code = 204
    description = "Unauthenticated"
    http_code = 401


class UserDontExist(ApiError):
    """ Got empty user on query from user_id in token """
    code = 205
    description = "User doesn't exist"
    http_code = 401


class InvalidToken(ApiError):
    """ Invalid token provided """
    code = 206
    description = "Invalid token"
    http_code = 403


class ReportNotPresented(ApiError):
    """ Report not found in database """
    code = 301
    description = "Report not presented in request or has invalid format"
    http_code = 422


class IndicatorGroupDoesNotExist(ApiError):
    """ Indicator group not found in database """
    code = 402
    description = "Indicator group does not exist"
    http_code = 404


class BotTokenDontExist(ApiError):
    """ Bot token not found in database """
    code = 503
    description = "Bot token does not exist"
    http_code = 404
