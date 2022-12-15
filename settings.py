from os import getenv

from dotenv import load_dotenv

load_dotenv()

DB_URI = getenv("DB_URI")

GITHUB_CLIENT_ID = getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = getenv("GITHUB_CLIENT_SECRET")

JWK_KEY_FILE = getenv("JWK_KEY_FILE") if getenv("JWK_KEY_FILE") is not None else "key.jwk"

SECRET_KEY = getenv("S3_SECRET_KEY")
ACCESS_KEY = getenv("S3_ACCESS_KEY")
BUCKET_NAME = getenv("S3_BUCKET_NAME")
REGION_NAME = getenv("S3_REGION_NAME")
ENDPOINT_URL = getenv("S3_ENDPOINT_URL")
REPORTS_FOLDER = getenv("S3_REPORTS_FOLDER") if getenv("S3_REPORTS_FOLDER") is not None else "reports"
S3_BASE_URL = getenv("S3_BASE_URL")

TELEGRAM_API_ID = int(getenv("TELEGRAM_API_ID"))
TELEGRAM_API_HASH = getenv("TELEGRAM_API_HASH")
TELEGRAM_SESSION_NAME = getenv("TELEGRAM_SESSION_NAME") if getenv("TELEGRAM_SESSION_NAME") is not None else "ioc"
