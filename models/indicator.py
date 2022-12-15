from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel
from tortoise import Model, fields

from models.report import ReportPD, Report
from models.users import UserPD, User


class IndicatorGroup(Model):
    """ ORM Model of Indicators Group """
    id = fields.UUIDField(pk=True)
    description = fields.TextField(null=True)
    owner = fields.ForeignKeyField('models.User')

    @staticmethod
    async def from_reports_collected_data(data, owner: User, report: Report = None):
        """ Creates indicators group from collected data

        Args:
            report: Optional report, bound to indicators group
            owner: Owner of indicators and indicators group
            data (CollectedData): Collected data from report
        """
        group = IndicatorGroup(
            description=None if report is None else f"Created from report {report.id}",
            owner=owner,
        )
        await group.save()
        indicators = data.indicators(owner=owner, indicator_group=group, report=report)
        await Indicator.bulk_create(indicators)
        return group


class IndicatorType(Enum):
    """ Enum type for Indicator """
    HASH = "HASH"
    IP_ADDRESS = "IP_ADDRESS"
    URL = "URL"


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

    class Config:
        orm_mode = True


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

    class Config:
        orm_mode = True
        fields = {
            "owner": {"exclude": True},
            "group": {"exclude": True},
            "report": {"exclude": True},
        }
