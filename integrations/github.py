from aiohttp import request

from responses.errors import GithubBadCodeError, GithubError
from settings import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET


class GithubAPI:
    @staticmethod
    async def process_code(oauth_code: str) -> str:
        """
            Returns access token from GitHub oauth callback code

            Args:
                oauth_code: str Oauth code
            Raises:
                GithubBadCodeError on incorrect oauth code
                GithubError on unexpected GitHub response
        """
        async with request("POST", "https://github.com/login/oauth/access_token", json={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": oauth_code
        }, headers={"Accept": "application/json"}) as resp:
            req_data = await resp.json()
            if "error" in req_data:
                if req_data["error"] == "bad_verification_code":
                    raise GithubBadCodeError
                else:
                    raise GithubError
            if resp.status != 200:
                raise GithubError
            return req_data["access_token"]

    @staticmethod
    async def get_user(access_token: str) -> dict:
        """
        Returns user by access_token and

        Args:
            access_token: GitHub access token

        Returns:
            GitHub username and user_id in dict with same name keys
        """
        async with request("GET", "https://api.github.com/user",
                           headers={"Accept": "application/json", "Authorization": f"Bearer {access_token}"}) as resp:
            data = await resp.json()
            if resp.status != 200 or "error" in data:
                raise GithubError
            return {
                "username": data["login"],
                "user_id": data["id"]
            }
