from fastapi import FastAPI, APIRouter
from database.db import init_db
from models.user import User
from dotenv import load_dotenv
from routers import clients
import os

load_dotenv

if not os.getenv("PFA_SECRET_KEY"):
    print("Missing PFA_SECRET_KEY variable")
    exit(1)

init_db()

app = FastAPI()

app.include_router(clients.router)

@app.get("/")
async def root():
    return {"message": "Welcome to PFA Manager API"}

@app.post("/signup")
async def signup_handler(user: User):
    added_user = user.add()
    if type(added_user) == User:
        return added_user

