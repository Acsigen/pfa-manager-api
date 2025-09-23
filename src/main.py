from fastapi import FastAPI
from .database import db
from .models.user import User
from dotenv import load_dotenv
from .routers import clients, contracts, work_orders, activity_reports, invoices
import os

load_dotenv()

if not os.getenv(key="PFA_SECRET_KEY"):
    print("Missing PFA_SECRET_KEY variable")
    exit(code=1)

db.init_db()

app: FastAPI = FastAPI()

app.include_router(router=clients.router)
app.include_router(router=contracts.router)
app.include_router(router=work_orders.router)
app.include_router(router=activity_reports.router)
app.include_router(router=invoices.router)

@app.get(path="/")
async def root():
    return {"message": "Welcome to PFA Manager API"}

@app.post(path="/signup")
async def signup_handler(user: User):
    added_user: User = user.add()
    if type(added_user) is User:
        return added_user

