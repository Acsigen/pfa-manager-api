from fastapi import APIRouter
from models.client import Client, delete_client as delete_client, list_clients as list_clients, show_client as show_client

router = APIRouter()

@router.post("/api/v1/clients")
async def add_client_handler(client: Client):
    added_client = client.add()
    if type(added_client) == Client:
        return added_client

@router.put("/api/v1/clients/{client_id}")
async def update_client_handler(client_id: int, client: Client):
    updated_client = client.update(client_id)
    if type(updated_client) == Client:
        return updated_client

@router.get("/api/v1/clients/{client_id}")
async def show_client_handler(client_id: int):
    client = show_client(client_id)
    if type(client) == Client:
        return client

@router.get("/api/v1/clients")
async def list_clients_handler():
    client_list = list_clients()
    if type(client_list) == list:
        return client_list

@router.delete("/api/v1/clients/{client_id}")
async def delete_client_handler(client_id: int):
    if delete_client(client_id=client_id) == True:
        return "Client deleted"