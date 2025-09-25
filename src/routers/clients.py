from fastapi import APIRouter, Depends
from ..models.client import Client, delete_client, list_user_clients, show_user_client
from .auth import get_current_user
from typing import Annotated

router: APIRouter = APIRouter(tags=["clients"])

user_dependency = Annotated[dict, Depends(dependency=get_current_user)]


@router.post(path="/api/v1/clients")
async def add_client_handler(user: user_dependency, client: Client):
    added_client: Client = client.add(user_id=user.get("user_id"))
    if type(added_client) is Client:
        return added_client


@router.put(path="/api/v1/clients/{client_id}")
async def update_client_handler(user: user_dependency, client_id: int, client: Client):
    updated_client: Client = client.update(
        client_id=client_id, user_id=user.get("user_id")
    )
    if type(updated_client) is Client:
        return updated_client


@router.get(path="/api/v1/clients/{client_id}")
async def show_client_handler(user: user_dependency, client_id: int):
    client: Client = show_user_client(client_id=client_id, user_id=user.get("user_id"))
    if type(client) is Client:
        return client


@router.get(path="/api/v1/clients")
async def list_user_clients_handler(user: user_dependency):
    client_list: list = list_user_clients(user_id=user.get("user_id"))
    if type(client_list) is list:
        return client_list


@router.delete(path="/api/v1/clients/{client_id}")
async def delete_client_handler(user: user_dependency, client_id: int):
    if delete_client(client_id=client_id, user_id=user.get("user_id")):
        return "Client deleted"
