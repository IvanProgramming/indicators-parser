import os
from uuid import uuid4
from tempfile import NamedTemporaryFile

from aiohttp import request as aiohttp_request
from starlette.background import BackgroundTasks
from starlette.datastructures import UploadFile
from starlette.requests import Request
from tortoise.expressions import Q

from integrations.s3 import save_report_to_s3, generate_report_url
from models import Report, IndicatorGroup
from models.indicator import IndicatorGroupPD
from models.report import ReportPD
from parsers.pdf_parser import process_pdf
from parsers.text_parser import CollectedData, find_ioc
from responses.errors import ReportNotPresented, ReportURLError, ReportNotFound
from responses.responses import OkResponse


async def load_report(request: Request):
    """ Parses the report and saves it to the database """
    report_id = str(uuid4())
    form = await request.form()
    try:
        file: UploadFile = form["file"]
    except KeyError:
        raise ReportNotPresented
    temp = NamedTemporaryFile(prefix="cs-report-", suffix=".pdf", delete=False)
    temp.file.write(await file.read())
    data: CollectedData = process_pdf(temp.name)
    report: Report = Report(
        id=report_id,
        owner=request.state.user,
        mime=file.content_type,
    )
    await report.save()
    group = await IndicatorGroup.from_reports_collected_data(data, request.state.user, report)
    group_pd = IndicatorGroupPD.from_orm(group)
    temp.close()
    background = BackgroundTasks()
    background.add_task(save_report_to_s3, temp.name, report_id)
    background.add_task(os.remove, temp.name)
    return OkResponse({"report_id": report_id, "indicator_group": group_pd}, background=background)


async def get_reports(request: Request):
    """ Returns user's reports """
    reports = await Report.filter(owner=request.state.user).all()
    as_pd = []
    for report in reports:
        report.owner = request.state.user
        as_pd.append(ReportPD.from_orm(report))
    return OkResponse(as_pd)


async def get_page_report(request: Request):
    """ Creates group from news page """
    url = request.query_params["url"]
    try:
        async with aiohttp_request("GET", url) as resp:
            page = await resp.text()
            if resp.status != 200:
                raise ReportURLError
    except Exception:
        raise ReportURLError
    data = find_ioc(page.lower())
    group = await IndicatorGroup.from_reports_collected_data(data, request.state.user)
    group.description = "Group from page " + url
    await group.save()
    group_pd = IndicatorGroupPD.from_orm(group)
    return OkResponse({"indicator_group": group_pd})


async def get_report_file(request: Request):
    """ Returns report file """
    try:
        report_id = request.query_params["report_id"]
    except KeyError:
        raise ReportNotFound
    report = await Report.get_or_none(id=report_id)
    if report is None or (report.owner_id != request.state.user.id and not report.is_public):
        raise ReportNotFound
    return OkResponse({"link": generate_report_url(report_id)})
