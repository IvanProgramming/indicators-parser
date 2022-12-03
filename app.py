from starlette.applications import Starlette
from loguru import logger
from endpoints.routes import routes


app = Starlette(routes=routes)

if __name__ == '__main__':
    from uvicorn import run

    logger.warning("For development purposes only. Use uvicorn in production")
    run("app:app", port=8080, log_level="debug", reload=True)
