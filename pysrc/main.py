from fastapi import FastAPI
from database.db import init_db
from models.user import User
from models.client import Client
from dotenv import load_dotenv
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
async def signup(user: User):
    user.create_user()

@app.post("/api/v1/clients")
async def signup(client: Client):
    client.create_client()