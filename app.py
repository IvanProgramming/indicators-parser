from os.path import exists

from loguru import logger
from starlette.applications import Starlette
from tortoise import Tortoise
from sys import argv

from auth.utils import create_and_save_key
from connection import init_database_connection
from endpoints.routes import routes
from responses.errors import ApiError, handle_api_error


async def on_start():
    """ This function is running on start of Starlette App """
    await init_database_connection()


async def on_stop():
    """ This function is running on stop of Starlette App """
    await Tortoise.close_connections()


app = Starlette(routes=routes, on_startup=[on_start], on_shutdown=[on_stop], exception_handlers={
    ApiError: handle_api_error
})

if __name__ == '__main__':
    if len(argv) >= 2:
        if argv[1] == "generate_key":
            if exists("key.jwk"):
                select = input("jwk.key already exists. Create new instead it? [y/N] ")
                if select.lower() != "y":
                    exit()
            create_and_save_key()
        else:
            logger.error("Unknown command")
    else:
        from uvicorn import run

        logger.warning("For development purposes only. Use uvicorn in production")
        run("app:app", port=8080, log_level="debug", reload=True)
