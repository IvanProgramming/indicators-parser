from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from tortoise import Model, fields

from models.report import ReportPD
from models.users import UserPD


class IndicatorGroup(Model):
    """ ORM Model of Indicators Group """
    id = fields.UUIDField(pk=True)
    description = fields.TextField(null=True)
    owner = fields.ForeignKeyField('models.User')


class IndicatorType(Enum):
    """ Enum type for Indicator """
    HASH = "HASH"
    DOMAIN = "DOMAIN"
    IP_ADDRESS = "IP_ADDRESS"


class Indicator(Model):
    """ ORM Model of Indicators """
    id = fields.UUIDField(pk=True)
    type = fields.CharEnumField(IndicatorType)
    value = fields.TextField()
    owner = fields.ForeignKeyField('models.User', on_delete=fields.SET_NULL, null=True)
    group = fields.ForeignKeyField('models.IndicatorGroup', on_delete=fields.SET_NULL, null=True)
    report = fields.ForeignKeyField('models.Report', on_delete=fields.SET_NULL, null=True)


class IndicatorGroupPD(BaseModel):
    """ Pydantic model of Indicator Group, might be used in http responses """

    id: UUID
    """ UUID-typed id of group """
    description: Optional[str]
    """ Optional description of group """
    owner: Optional[UserPD]
    """ Group owner """


class IndicatorPD(BaseModel):
    """ Pydantic model of Indicator, might be used in http responses """

    id: UUID
    """ ID of Indicator """
    type: IndicatorType
    """ Type of indicator, like HASH or DOMAIN  """
    value: str
    """ Raw value of indicator """
    owner: Optional[UserPD]
    """ Owner of indicator, on delete becomes NULL """
    group: Optional[IndicatorGroupPD]
    """ Group, that has this indicator as its member, NULL on unset """
    report: Optional[ReportPD]
    """ Report, that was parsed to get this indicator, NULL on unset """
