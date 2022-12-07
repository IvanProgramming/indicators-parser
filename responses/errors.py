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
