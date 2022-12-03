from starlette.routing import Route
from endpoints import ping
unauthenticated_routes = [
    Route("/ping", ping, methods=["GET"])
]

api_available_routes = []

user_only_routes = []

admin_routes = []

routes = unauthenticated_routes + api_available_routes + user_only_routes
