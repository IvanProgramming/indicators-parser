from loguru import logger
from starlette.applications import Starlette
from tortoise import Tortoise

from connection import init_database_connection
from endpoints.routes import routes
from models import User


async def on_start():
    """ This function is running on start of Starlette App """
    await init_database_connection()


async def on_stop():
    """ This function is running on stop of Starlette App """
    await Tortoise.close_connections()


app = Starlette(routes=routes, on_startup=[on_start])

if __name__ == '__main__':
    from uvicorn import run

    logger.warning("For development purposes only. Use uvicorn in production")
    run("app:app", port=8080, log_level="debug", reload=True)
