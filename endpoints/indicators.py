from starlette.requests import Request
from tortoise.exceptions import DoesNotExist

from models import IndicatorGroup, Indicator
from models.indicator import IndicatorPD, IndicatorGroupPD
from models.users import UserPD
from responses.errors import IndicatorGroupDoesNotExist
from responses.responses import OkResponse


async def get_indicators_from_group(request: Request):
    """ Get indicators from indicator group """
    group_id = request.query_params["group_id"]
    page = int(request.query_params.get("page", 1))
    try:
        group = await IndicatorGroup.get(id=group_id, owner=request.state.user)
        group.owner = request.state.user
        group_pd = IndicatorGroupPD.from_orm(group)
    except DoesNotExist:
        raise IndicatorGroupDoesNotExist
    indicators = await Indicator.filter(group=group).limit(10).offset((page - 1) * 10).all()
    indicators_pd = []
    for indicator in indicators:
        indicator.group = None
        indicator.owner = None
        indicator.report = None
        indicators_pd.append(IndicatorPD.from_orm(indicator))
    return OkResponse({"indicators": indicators_pd, "group": group_pd})


async def get_indicator_groups(request: Request):
    """ Get all groups that belongs to user """
    groups = await IndicatorGroup.filter(owner=request.state.user).all()
    groups_pd = []
    for group in groups:
        group.owner = request.state.user
        groups_pd.append(IndicatorGroupPD.from_orm(group))
    return OkResponse(groups_pd)
