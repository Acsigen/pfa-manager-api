from fastapi import APIRouter, Depends
from ..models.work_order import (
    WorkOrder,
    show_work_order,
    list_work_orders,
    delete_user_work_order,
)
from .auth import get_current_user
from typing import Annotated

router: APIRouter = APIRouter(tags=["work_orders"])

user_dependency = Annotated[dict, Depends(dependency=get_current_user)]


@router.post(path="/api/v1/clients/{client_id}/contracts/{contract_id}/wo")
async def add_work_order_handler(
    user: user_dependency,client_id: int, contract_id: int, work_order: WorkOrder
):
    added_work_order: WorkOrder = work_order.add(
        contract_id=contract_id, client_id=client_id, user_id=user.get("user_id")
    )
    if type(added_work_order) is WorkOrder:
        return added_work_order


@router.put(path="/api/v1/clients/{client_id}/contracts/{contract_id}/wo/{wo_id}")
async def update_work_order_handler(
    user: user_dependency, client_id: int, contract_id: int, wo_id: int, work_order: WorkOrder
):
    updated_work_order: WorkOrder = work_order.update(
        client_id=client_id, contract_id=contract_id, work_order_id=wo_id, user_id=user.get("user_id")
    )
    if type(updated_work_order) is WorkOrder:
        return updated_work_order


@router.get(path="/api/v1/clients/{client_id}/contracts/{contract_id}/wo/{wo_id}")
async def show_work_order_handler(user: user_dependency, client_id: int, contract_id: int, wo_id: int):
    work_order: WorkOrder = show_work_order(
        client_id=client_id, contract_id=contract_id, work_order_id=wo_id, user_id=user.get("user_id")
    )
    if type(work_order) is WorkOrder:
        return work_order


@router.get(path="/api/v1/clients/{client_id}/contracts/{contract_id}/wo")
async def list_work_orders_handler(user: user_dependency, client_id: int, contract_id: int):
    contract_list: list[WorkOrder] = list_work_orders(
        client_id=client_id, contract_id=contract_id, user_id=user.get("user_id")
    )
    if type(contract_list) is list:
        return contract_list


@router.delete("/api/v1/clients/{client_id}/contracts/{contract_id}/wo/{wo_id}")
async def delete_work_order_handler(
    user: user_dependency, client_id: int, contract_id: int, wo_id: int
):
    if delete_user_work_order(client_id=client_id, contract_id=contract_id, work_order_id=wo_id) is True:
        return "Work order deleted"
