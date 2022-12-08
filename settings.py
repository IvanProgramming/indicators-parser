from os import getenv

from dotenv import load_dotenv

load_dotenv()

DB_URI = getenv("DB_URI")

OWNER_GITHUB_USERNAME = getenv("GITHUB_OWNER_USERNAME")

GITHUB_CLIENT_ID = getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = getenv("GITHUB_CLIENT_SECRET")

JWK_KEY_FILE = getenv("JWK_KEY_FILE") if getenv("JWK_KEY_FILE") is not None else "key.jwk"
