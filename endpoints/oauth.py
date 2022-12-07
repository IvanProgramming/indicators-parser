from starlette.requests import Request
from starlette.responses import RedirectResponse
from settings import GITHUB_CLIENT_ID

from integrations.github import GithubAPI
from responses.errors import NoGithubCode


async def github_oauth_callback(request: Request):
    """ GitHub OAuth callback request """
    if "code" not in request.query_params:
        raise NoGithubCode
    github_code = request.query_params["code"]
    access_token = await GithubAPI.process_code(github_code)
    github_data = await GithubAPI.get_user(access_token)
    return RedirectResponse("/", 301, headers={
        "Set-Cookie":
            f"token=[user={github_data['user_id']}&login={github_data['username']}]"  # TODO: save token to cookies
    })


async def github_oauth_redirect(request: Request):
    """ Redirect to GitHub OAuth login window """
    return RedirectResponse(f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}", 301)
