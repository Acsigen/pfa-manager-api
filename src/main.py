from fastapi import FastAPI
from .database import db
from .routers import clients, contracts, work_orders, activity_reports, invoices, auth
from dotenv import load_dotenv
from os import getenv

load_dotenv()

if not getenv(key="SECRET_KEY"):
    print("Missing SECRET_KEY. Exiting...")
    exit(code=1)

db.init_db()

app: FastAPI = FastAPI()

app.include_router(router=auth.router)
app.include_router(router=clients.router)
app.include_router(router=contracts.router)
app.include_router(router=work_orders.router)
app.include_router(router=activity_reports.router)
app.include_router(router=invoices.router)

@app.get(path="/")
async def root():
    return {"message": "Welcome to PFA Manager API"}
