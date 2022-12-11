from starlette.middleware import Middleware
from starlette.routing import Route, Mount

from endpoints import *
from auth.middleware import JWTAuthenticationMiddleware

unauthenticated_routes = [
    Route("/ping", ping, methods=["GET"]),
    Route("/login/github", github_oauth_redirect, methods=["GET"]),
    Route("/oauth/github", github_oauth_callback, methods=["GET"])
]

api_routes = [
    Route("/getMe", get_me, methods=["GET"]),
]

admin_routes = []

routes = [
    Mount(
        "/api", routes=api_routes,
        middleware=[Middleware(JWTAuthenticationMiddleware)]
    ),
    Mount(
        "/", routes=unauthenticated_routes,
    )
]
