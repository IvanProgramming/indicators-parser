from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from tortoise import Model, fields

from models.users import UserPD


class Report(Model):
    """ ORM Model of Loaded for parsing report """
    id = fields.UUIDField(pk=True)
    owner = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE)
    mime = fields.CharField(max_length=64)
    loaded_at = fields.DatetimeField(auto_now=True)
    is_public = fields.BooleanField(default=False)


class ReportPD(BaseModel):
    """ Pydantic model of report, might be used in http responses """

    id: UUID
    """ ID of Indicator """
    owner: UserPD
    """ User, that loaded this report """
    mime: str
    """ Mime type of report """
    loaded_at: datetime
    """ Date and time of loading report """
    is_public: bool
    """ Flag, shows, might this report and all indicators from it become public """

    class Config:
        orm_mode = True
        fields = {
            "is_public": {"exclude": True}
        }
