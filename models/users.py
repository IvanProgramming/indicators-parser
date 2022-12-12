from datetime import datetime, timedelta
from uuid import uuid4

from jwcrypto.jwt import JWT
from pydantic import BaseModel
from tortoise import Model, fields
from auth.key import key, decrypt_token
from responses.errors import UserDontExist


class User(Model):
    """ ORM model of User """
    id = fields.IntField(pk=True)
    github_user_id = fields.IntField(unique=True)
    github_username = fields.CharField(max_length=64)
    is_admin = fields.BooleanField(default=False)
    is_private = fields.BooleanField(default=False)

    def create_token(self, for_bot=False) -> str:
        """ Creates JWT token for user """
        claims = {
            "user_id": self.id,
            "exp": int((datetime.now() + timedelta(days=30)).timestamp()),
            "iss": "ioc"
        }
        if for_bot:
            claims["bot_token_id"] = str(uuid4())
        jwt = JWT(header={"alg": "RS256"}, claims=claims)
        jwt.make_signed_token(key.jwk)
        return jwt.serialize()

    @staticmethod
    async def generate_id() -> int:
        """ Creates new ID for user, according to all existing users """
        user = await User.all().order_by("-id").first()
        if user is None:
            return 1
        return user.id + 1

    class Meta:
        table = "users"


class UserPD(BaseModel):
    """ Model of user, can be used in response """

    id: int
    """ Unique ID of user """
    github_user_id: int
    """ ID of GitHub user """
    github_username: str
    """ Attached GitHub account username """
    is_admin: bool
    """ Flag, shows, if user is admin """
    is_private: bool
    """ Flag, shows, if user profile is public """

    class Config:
        orm_mode = True
        fields = {
            'is_admin': {'exclude': True},
            'is_private': {'exclude': True}
        }


class BotToken(Model):
    """ ORM model of Bot Token """
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE)
    expires_at = fields.DatetimeField()
    created_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "bot_tokens"

    @staticmethod
    async def create_from_token(token: str, expires_in: int = 30) -> 'BotToken':
        """ Creates new bot token from token

        Args:
            token: Token, which will be used to create bot token
            expires_in: Time in days, when token will be expired
        """
        data = decrypt_token(token)
        user = await User.get_or_none(id=data["user_id"])
        if user is None:
            raise UserDontExist
        return await BotToken.create(user=user, id=data["bot_token_id"],
                                     expires_at=datetime.now() + timedelta(days=expires_in))
