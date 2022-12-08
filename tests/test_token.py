from models.users import User
from auth.utils import create_and_save_key
from auth.key import key, decrypt_token


def test_token_generation():
    create_and_save_key("test_key.jwk")
    key.load_key("test_key.jwk")

    user = User(id=54, github_user_id=100, github_username="krol")
    token = user.create_token()

    claims = decrypt_token(token)

    assert claims["user_id"] == 54
