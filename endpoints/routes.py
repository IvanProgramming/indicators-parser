from starlette.middleware import Middleware
from starlette.routing import Route, Mount

from endpoints import *
from auth.middleware import JWTAuthenticationMiddleware

unauthenticated_routes = [
    Route("/ping", ping, methods=["GET"]),
    Route("/login/github", github_oauth_redirect, methods=["GET"]),
    Route("/oauth/github", github_oauth_callback, methods=["GET"]),
    Route("/token", token, methods=["GET"]),
]

api_routes = [
    Route("/getMe", get_me, methods=["GET"]),
    Route("/loadReport", load_report, methods=["POST"]),
    Route("/getIndicatorsFromGroup", get_indicators_from_group, methods=["GET"]),
    Route("/createBotToken", create_bot_token, methods=["GET"]),
    Route("/getBotTokens", get_bot_tokens, methods=["GET"]),
    Route("/deleteBotToken", delete_bot_token, methods=["GET"]),
    Route("/createWatcher", create_watcher, methods=["POST"]),
    Route("/getIndicatorGroups", get_indicator_groups, methods=["GET"]),
    Route("/getReports", get_reports, methods=["GET"]),
    Route("/getReportFilePath", get_report_file, methods=["GET"]),
    Route("/loadPageReport", get_page_report, methods=["GET"]),
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
