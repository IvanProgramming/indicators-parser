from starlette.routing import Route

from endpoints import *

unauthenticated_routes = [
    Route("/ping", ping, methods=["GET"]),
    Route("/login/github", github_oauth_redirect, methods=["GET"]),
    Route("/oauth/github", github_oauth_callback, methods=["GET"])
]

api_available_routes = []

user_only_routes = []

admin_routes = []

routes = unauthenticated_routes + api_available_routes + user_only_routes + admin_routes
