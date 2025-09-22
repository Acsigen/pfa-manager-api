from fastapi import FastAPI, HTTPException
from database.db import init_db
from models.user import User
from models.client import Client, delete_client as delete_client, list_clients as list_clients, show_client as show_client
from dotenv import load_dotenv
from typing import List
import os

load_dotenv

if not os.getenv("PFA_SECRET_KEY"):
    print("Missing PFA_SECRET_KEY variable")
    exit(1)

init_db()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to PFA Manager API"}

@app.post("/signup")
async def signup_handler(user: User):
    user.add()

@app.post("/api/v1/clients")
async def add_client_handler(client: Client):
    client.add()

@app.put("/api/v1/clients/{client_id}")
async def update_client_handler(client_id: int, client: Client):
    updated_client = client.update(client_id)
    if type(updated_client) == Client:
        return updated_client
    else:
        raise HTTPException(500,updated_client)

@app.get("/api/v1/clients/{client_id}")
async def show_client_handler(client_id: int):
    client = show_client(client_id)
    if type(client) == Client:
        return client
    else:
        raise HTTPException(500,client)


@app.get("/api/v1/clients")
async def list_clients_handler():
    client_list = list_clients()
    if type(client_list) == list:
        return client_list
    else:
        raise HTTPException(500,client_list)

@app.delete("/api/v1/clients/{client_id}")
async def delete_client_handler(client_id: int):
    delete_client(client_id=client_id)