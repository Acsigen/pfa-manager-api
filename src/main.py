from fastapi import FastAPI
from .database import db
from .routers import clients, contracts, work_orders, activity_reports, invoices, auth

db.init_db()

app: FastAPI = FastAPI()

app.include_router(router=clients.router)
app.include_router(router=contracts.router)
app.include_router(router=work_orders.router)
app.include_router(router=activity_reports.router)
app.include_router(router=invoices.router)
app.include_router(router=auth.router)

@app.get(path="/")
async def root():
    return {"message": "Welcome to PFA Manager API"}
