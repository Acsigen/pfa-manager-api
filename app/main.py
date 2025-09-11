from fastapi import FastAPI, HTTPException
from controllers.sqlite import DBConnection
from models.Client import Client

app = FastAPI()

db = DBConnection("./data/sqlite.db")

@app.get("/")
async def root():
    """
    Welcome message
    """
    return {"message": "Welcome to PFA Manager API."}

@app.get("/clients")
async def get_all_clients():
    """
    Retrieve a list of clients
    """
    client_list = db.get_all_clients()
    return client_list

@app.get("/clients/{client_id}")
async def get_client_id(client_id):
    """
    Get the details of the client with ID taken from a path parameter
    """
    client_data = db.get_client_by_id(client_id)
    return client_data

@app.get("/clients/")
async def get_client_cui(cui : int):
    """
    Get the details of the client with CUI taken from a path parameter
    """
    client_data = db.get_client_by_cui(cui)
    return client_data

@app.post("/clients")
async def create_client(client: Client):
    """
    Add a new client
    """
    resp = db.add_client(client.model_dump())
    return resp

@app.put("/clients")
async def update_client(client: Client):
    """
    Update a client details based on ID
    """
    if not client.id:
        raise HTTPException(status_code=400, detail="id parameter is missing")
    else:
        resp = db.update_client(client.model_dump())
        return resp