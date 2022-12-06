from pydantic import BaseModel
from tortoise import Model, fields


class User(Model):
    """ ORM model of User """
    id = fields.IntField(pk=True)
    github_user_id = fields.IntField(unique=True)
    github_username = fields.CharField(max_length=64)
    is_admin = fields.BooleanField(default=False)
    is_private = fields.BooleanField(default=False)

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
