from pydantic import BaseModel
from fastapi import HTTPException
import sqlite3  # For error handling
from ..database import db
from .activity_report import ActivityReport

class InvoiceItem(BaseModel):
    id: int | None = None
    ar_id: int
    invoice_id: int | None = None

    def add(self):
        query = "INSERT INTO invoice_items(ar_id, invoice_id) VALUES (?,?)"
        data: tuple = (self.ar_id, self.invoice_id)
        try:
            res: sqlite3.Cursor = db.execute_query(query=query, params=data)
            self.id = res.lastrowid
            return self
        except sqlite3.IntegrityError as e:
            raise HTTPException(status_code=500, detail=e.args[0])
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=e.args[0])
        
def delete_invoice_item(item_id: int):
    query = "DELETE FROM invoice_items WHERE id == ?"
    data: tuple = (item_id,)
    try:
        _: sqlite3.Cursor = db.execute_query(query=query, params=data)
        return True
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=e.args[0])

def get_invoice_available_items(client_id: int, invoice_id: int, user_id: int):
    permitted_action: bool = check_permissions(
            client_id=client_id, current_user_id=user_id
        )
    if permitted_action:
        available_items: list[ActivityReport] = []
        query = """
        SELECT DISTINCT
            ar.id,
            ar.wo_id,
            ar.name,
            ar.date,
            ar.hours_amount,
            ar.user_id
        FROM activity_reports ar
        INNER JOIN work_orders wo ON ar.wo_id = wo.id
        INNER JOIN contracts c ON wo.contract_id = c.id
        INNER JOIN invoices i ON i.client_id = c.client_id
        WHERE i.id = ?
            AND ar.user_id = ?
            AND ar.id NOT IN (
                SELECT ar_id 
                FROM invoice_items
            )
        ORDER BY ar.date DESC;
        """
        data: tuple = (invoice_id,user_id)
        try:
            res: sqlite3.Cursor = db.execute_query(query=query, params=data)
            rows: list[tuple] = res.fetchall()
            for row in rows:
                activity_report: ActivityReport = ActivityReport(
                    id=int(row[0]),
                        wo_id=row[1],
                        name=row[2],
                        date=row[3],
                        hours_amount=row[4],
                        user_id=row[5],
                )
                available_items.append(activity_report)
            return available_items
        except sqlite3.OperationalError as e:
            raise HTTPException(status_code=500, detail=e.args[0])

def get_invoice_items(client_id: int, invoice_id: int, user_id: int):
    permitted_action: bool = check_permissions(
            client_id=client_id, current_user_id=user_id
        )
    if permitted_action:
        invoice_items: list[dict] = []
        query = """
        SELECT c.contract_no,
        wo.name,
        ar.hours_amount,
        wo.price,
        wo.currency 
        FROM activity_reports ar
        INNER JOIN work_orders wo ON ar.wo_id = wo.id
        INNER JOIN contracts c ON wo.contract_id = c.id
        INNER JOIN invoices i ON i.client_id = c.client_id
        WHERE i.id = ?
            AND ar.user_id = ?
            AND ar.id IN (
                SELECT ar_id 
                FROM invoice_items
            )
        ORDER BY ar.date DESC;
        """
        data: tuple = (invoice_id, user_id)
        try:
            res: sqlite3.Cursor = db.execute_query(query=query, params=data)
            rows: list[tuple] = res.fetchall()
            for row in rows:
                invoice_item: dict = {
                    "contract_no": row[0],
                    "wo_name": row[1],
                    "hours_amount": float(row[2]),
                    "price": float(row[3]),
                    "currency": row[4]
                }
                
                invoice_items.append(invoice_item)
            return invoice_items
        except sqlite3.OperationalError as e:
            raise HTTPException(status_code=500, detail=e.args[0])

class Invoice(BaseModel):
    id: int | None = None
    name: str
    currency: str
    exchange_rate: float
    invoice_date: str
    due_date: str
    status: str
    client_id: int
    user_id: int | None = None

    def add(self, user_id: int):
        permitted_action: bool = check_permissions(
            client_id=self.client_id, current_user_id=user_id
        )
        if permitted_action:
            query = "INSERT INTO invoices(name, currency, exchange_rate, invoice_date, due_date, status, client_id, user_id) VALUES (?,?,?,?,?,?,?,?)"
            self.user_id = user_id
            data: tuple = (
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
                raise HTTPException(status_code=500, detail=e.args[0])

    def update(self, user_id: int, invoice_id: int):
        permitted_action: bool = check_permissions(
            client_id=self.client_id, current_user_id=user_id, invoice_id=invoice_id
        )
        if permitted_action:
            query = "UPDATE invoices SET name = ?, currency = ?, exchange_rate = ?, invoice_date = ?, due_date = ?, status =?	WHERE id = ? AND user_id = ?"
            self.user_id = user_id
            self.id = invoice_id
            data: tuple = (
                self.name,
                self.currency,
                self.exchange_rate,
                self.invoice_date,
                self.due_date,
                self.status,
                self.id,
                self.user_id
            )
            try:
                _: sqlite3.Cursor = db.execute_query(query=query, params=data)
                return self
            except sqlite3.IntegrityError as e:
                raise HTTPException(status_code=500, detail=e.args[0])


def show_invoice(user_id:int, invoice_id: int):
    query = "SELECT * FROM invoices WHERE id == ? AND user_id = ?"
    data: tuple = (invoice_id, user_id)
    try:
        res: sqlite3.Cursor = db.execute_query(query=query, params=data)
        row: tuple = res.fetchone()
        invoice: Invoice = Invoice(
            id=int(row[0]),
            name=row[1],
            client_id=int(row[2]),
            currency=row[3],
            exchange_rate=row[4],
            invoice_date=row[5],
            due_date=row[6],
            status=row[7],
            user_id=int(row[8]),
        )
        return invoice
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=500, detail=e.args[0])


def list_user_invoices(user_id: int):
    invoice_list: list[Invoice] = []
    query = "SELECT * FROM invoices WHERE user_id = ? ORDER BY invoice_date DESC"
    data: tuple = (user_id,)
    try:
        res: sqlite3.Cursor = db.execute_query(query=query, params=data)
        rows: list[tuple] = res.fetchall()
        for row in rows:
            invoice: Invoice = Invoice(
                id=int(row[0]),
                name=row[1],
                client_id=int(row[2]),
                currency=row[3],
                exchange_rate=row[4],
                invoice_date=row[5],
                due_date=row[6],
                status=row[7],
                user_id=int(row[8]),
            )
            invoice_list.append(invoice)
        return invoice_list
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail=e.args[0])

def list_client_invoices(client_id:int, user_id: int):
    permitted_action: bool = check_permissions(
            client_id=client_id, current_user_id=user_id
        )
    if permitted_action:
        invoice_list: list[Invoice] = []
        query = "SELECT * FROM invoices WHERE user_id = ? AND client_id = ?"
        data: tuple = (user_id,client_id)
        try:
            res: sqlite3.Cursor = db.execute_query(query=query, params=data)
            rows: list[tuple] = res.fetchall()
            for row in rows:
                invoice: Invoice = Invoice(
                    id=int(row[0]),
                    name=row[1],
                    client_id=int(row[2]),
                    currency=row[3],
                    exchange_rate=row[4],
                    invoice_date=row[5],
                    due_date=row[6],
                    status=row[7],
                    user_id=int(row[8]),
                )
                invoice_list.append(invoice)
            return invoice_list
        except sqlite3.OperationalError as e:
            raise HTTPException(status_code=500, detail=e.args[0])

def check_permissions(
    client_id: int, current_user_id: int, invoice_id: int | None = None
):
    if invoice_id:
        query = """SELECT inv.user_id
            FROM invoices AS inv
            JOIN clients AS cli on inv.client_id = cli.id
            WHERE inv.id = ? AND cli.id = ?"""
        data: tuple = (invoice_id, client_id)
    else:
        query = "SELECT user_id FROM clients WHERE id == ?"
        data: tuple = (client_id,)
    try:
        res: sqlite3.Cursor = db.execute_query(query=query, params=data)
        row: tuple = res.fetchone()
        if row:
            retrieved_user_id: int = int(row[0])
        else:
            raise HTTPException(
                status_code=403, detail="You are not allowed to perform this action"
            )
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=e.args[0])
    if retrieved_user_id == current_user_id:
        return True
    else:
        raise HTTPException(
            status_code=403, detail="You are not allowed to perform this action"
        )
