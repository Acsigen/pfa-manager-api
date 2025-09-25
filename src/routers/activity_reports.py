from fastapi import APIRouter, Depends
from ..models.activity_report import (
    ActivityReport,
    show_activity_report,
    list_activity_reports,
    delete_activity_report,
)
from .auth import get_current_user
from typing import Annotated

router: APIRouter = APIRouter(tags=["activity_reports"])

user_dependency = Annotated[dict, Depends(dependency=get_current_user)]


@router.post(path="/api/v1/clients/{client_id}/contracts/{contract_id}/wo/{wo_id}/ar")
async def add_activity_report_handler(
    user: user_dependency, wo_id: int, activity_report: ActivityReport
):
    added_activity_report: ActivityReport = activity_report.add(
        wo_id=wo_id, user_id=user.get("user_id")
    )
    if type(added_activity_report) is ActivityReport:
        return added_activity_report


@router.put(
    path="/api/v1/clients/{client_id}/contracts/{contract_id}/wo/{wo_id}/ar/{ar_id}"
)
async def update_activity_report_handler(
    user: user_dependency, wo_id: int, ar_id: int, activity_report: ActivityReport
):
    updated_activity_report: ActivityReport = activity_report.update(
        wo_id=wo_id, ar_id=ar_id, user_id=user.get("user_id")
    )
    if type(updated_activity_report) is ActivityReport:
        return updated_activity_report


@router.get(
    path="/api/v1/clients/{client_id}/contracts/{contract_id}/wo/{wo_id}/ar/{ar_id}"
)
async def show_activity_report_handler(user: user_dependency, wo_id: int, ar_id: int):
    activity_report: ActivityReport = show_activity_report(
        wo_id=wo_id, activity_report_id=ar_id, user_id=user.get("user_id")
    )
    if type(activity_report) is ActivityReport:
        return activity_report


@router.get(path="/api/v1/clients/{client_id}/contracts/{contract_id}/wo/{wo_id}/ar")
async def list_activity_reports_handler(user: user_dependency, wo_id: int):
    contract_list: list[ActivityReport] = list_activity_reports(
        wo_id=wo_id, user_id=user.get("user_id")
    )
    if type(contract_list) is list:
        return contract_list


@router.delete(
    "/api/v1/clients/{client_id}/contracts/{contract_id}/wo/{wo_id}/ar/{ar_id}"
)
async def delete_activity_report_handler(user: user_dependency, wo_id: int, ar_id: int):
    if (
        delete_activity_report(
            wo_id=wo_id, activity_report_id=ar_id, user_id=user.get("user_id")
        )
        is True
    ):
        return "Activity report deleted"
