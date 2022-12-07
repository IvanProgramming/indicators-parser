from responses.responses import BadResponse


class ApiError(Exception):
    """ Base API error """
    code: int
    description: str
    http_code: int = 500

    def as_response(self):
        """ Error as a response """
        return BadResponse(self.code, self.description, self.http_code)


class GithubBadCodeError(ApiError):
    """ GitHub callback code error """
    code = 101
    description = "Github authorization code is incorrect"
    http_code = 412


class GithubError(ApiError):
    """ GitHub internal bad response """
    code = 102
    description = "Github authorization error"
    http_code = 500
