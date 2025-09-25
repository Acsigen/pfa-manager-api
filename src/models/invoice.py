from pydantic import BaseModel
from fastapi import HTTPException
import sqlite3  # For error handling
from ..database import db


class Invoice(BaseModel):
    id: int | None = None
    name: str
    currency: str
    exchange_rate: float
    invoice_date: str
    due_date: str
    status: str
    client_id: int | None = 0
    user_id: int | None = None

    def add(self):
        query = "INSERT INTO invoices(name, currency, exchange_rate, invoice_date, due_date, status, client_id, user_id) VALUES (?,?,?,?,?,?,?,?)"
        self.user_id = 0
        data = (
            self.name,
            self.currency,
            self.exchange_rate,
            self.invoice_date,
            self.due_date,
            self.status,
            self.client_id,
            self.user_id,
        )
        try:
            res: sqlite3.Cursor = db.execute_query(query=query, params=data)
            self.id = res.lastrowid
            return self
        except sqlite3.IntegrityError as e:
            raise HTTPException(500, e.args[0])

    def update(self, invoice_id):
        query = "UPDATE invoices SET currency = ?, exchange_rate = ?, invoice_date = ?, due_date = ?, status =?	WHERE id = ?"
        self.user_id = 0
        self.id = invoice_id
        data = (
            self.name,
            self.currency,
            self.exchange_rate,
            self.invoice_date,
            self.due_date,
            self.status,
            self.id,
        )
        try:
            _: sqlite3.Cursor = db.execute_query(query=query, params=data)
            return self
        except sqlite3.IntegrityError as e:
            raise HTTPException(500, e.args[0])


def show_invoice(invoice_id: int):
    query = "SELECT * FROM invoices WHERE id == ?"
    data = (invoice_id,)
    try:
        res: sqlite3.Cursor = db.execute_query(query=query, params=data)
        row: tuple = res.fetchone()
        invoice: Invoice = Invoice(
            id=int(row[0]),
            name=row[1],
            currency=row[2],
            exchange_rate=row[3],
            invoice_date=row[4],
            due_date=row[5],
            status=row[6],
            client_id=row[7],
            user_id=row[8],
        )
        return invoice
    except sqlite3.IntegrityError as e:
        raise HTTPException(500, e.args[0])


def list_invoices():
    invoice_list: list[Invoice] = []
    query = "SELECT * FROM invoices"
    try:
        res: sqlite3.Cursor = db.execute_query(query=query)
        rows: list[tuple] = res.fetchall()
        for row in rows:
            invoice: Invoice = Invoice(
                id=int(row[0]),
                name=row[1],
                currency=row[2],
                exchange_rate=row[3],
                invoice_date=row[4],
                due_date=row[5],
                status=row[6],
                client_id=row[7],
                user_id=row[8],
            )
            invoice_list.append(invoice)
        return invoice_list
    except sqlite3.OperationalError as e:
        raise HTTPException(500, e.args[0])


def delete_invoice(invoice_id: int):
    query = "DELETE FROM invoices WHERE id == ?"
    data: tuple[int] = (invoice_id,)
    try:
        _: sqlite3.Cursor = db.execute_query(query=query, params=data)
        return True
    except sqlite3.IntegrityError as e:
        raise HTTPException(500, e.args[0])
