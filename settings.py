from os import getenv

from dotenv import load_dotenv

load_dotenv()

DB_URI = getenv("DB_URI")

OWNER_GITHUB_USERNAME = getenv("GITHUB_OWNER_USERNAME")
