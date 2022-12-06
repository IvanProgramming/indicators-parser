from tortoise import Tortoise

from settings import DB_URI


async def init_database_connection(db_uri: str = None):
    """
        Connects to database with given db_uri and loads models into DB

        Parameters:
            db_uri: Optional. Database URI with

    """
    if db_uri is None:
        db_uri = DB_URI
    await Tortoise.init(
        db_url=db_uri,
        modules={"models": ['models']}
    )
    await Tortoise.generate_schemas(
        safe=True
    )
