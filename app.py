from os.path import exists

from loguru import logger
from starlette.applications import Starlette
from sys import argv

from tortoise.contrib.starlette import register_tortoise

from auth.key import key
from auth.utils import create_and_save_key
from endpoints.routes import routes
from responses.errors import ApiError, handle_api_error
from settings import DB_URI
from integrations.telegram import start, client

app = Starlette(routes=routes, on_startup=[key.load_key, start],
                exception_handlers={
                    ApiError: handle_api_error
                })

register_tortoise(app, config={
    'connections': {
        'default': DB_URI
    },
    'apps': {
        'models': {
            'models': ['models'],
            'default_connection': 'default',
        }
    }
}, generate_schemas=True)

if __name__ == '__main__':
    if len(argv) >= 2:
        if argv[1] == "generate_key":
            if exists("key.jwk"):
                select = input("jwk.key already exists. Create new instead it? [y/N] ")
                if select.lower() != "y":
                    exit()
            create_and_save_key()
        elif argv[1] == "generate_client":
            client.start()
            exit()
        else:
            logger.error("Unknown command")
    else:
        from uvicorn import run

        logger.warning("For development purposes only. Use uvicorn in production")
        run("app:app", port=8080, log_level="debug", reload=True)
