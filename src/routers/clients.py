from fastapi import APIRouter
from ..models.client import Client, delete_client, list_clients, show_client

router: APIRouter = APIRouter()

@router.post(path="/api/v1/clients")
async def add_client_handler(client: Client):
    added_client: Client = client.add()
    if type(added_client) is Client:
        return added_client

@router.put(path="/api/v1/clients/{client_id}")
async def update_client_handler(client_id: int, client: Client):
    updated_client: Client = client.update(client_id=client_id)
    if type(updated_client) is Client:
        return updated_client

@router.get(path="/api/v1/clients/{client_id}")
async def show_client_handler(client_id: int):
    client: Client = show_client(client_id=client_id)
    if type(client) is Client:
        return client

@router.get(path="/api/v1/clients")
async def list_clients_handler():
    client_list: list = list_clients()
    if type(client_list) is list:
        return client_list

@router.delete(path="/api/v1/clients/{client_id}")
async def delete_client_handler(client_id: int):
    if delete_client(client_id=client_id):
        return "Client deleted"