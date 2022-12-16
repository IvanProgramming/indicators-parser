from starlette.requests import Request
from starlette.responses import RedirectResponse

from models import User
from tortoise.exceptions import DoesNotExist
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
    try:
        user = await User.get(github_user_id=github_data["user_id"])
        token = user.create_token()
    except DoesNotExist:
        user = User(
            id=await User.generate_id(),
            github_user_id=github_data["user_id"],
            github_username=github_data["username"]
        )
        await user.save()
        token = user.create_token()
    resp = RedirectResponse("/token", 301)
    resp.set_cookie("token", token)
    return resp


async def github_oauth_redirect(request: Request):
    """ Redirect to GitHub OAuth login window """
    return RedirectResponse(f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}", 301)
