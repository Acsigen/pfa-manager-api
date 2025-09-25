from pydantic import BaseModel
from fastapi import HTTPException
import sqlite3
from ..database import db


class WorkOrder(BaseModel):
    id: int | None = None
    contract_id: int | None = None
    name: str
    final_client: str
    client_project_code: str | None = "N/A"
    start_date: str
    end_date: str
    price: float
    currency: str
    measurement_unit: str
    status: str | None = None
    user_id: int | None = None

    def add(self, client_id: int, contract_id: int, user_id: int):
        permitted_action: bool = check_permissions(
            client_id=client_id, contract_id=contract_id, current_user_id=user_id
        )
        if permitted_action:
            query = "INSERT INTO work_orders(contract_id, name, final_client, client_project_code, start_date, end_date, price, currency, measurement_unit, status, user_id) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
            self.contract_id = contract_id
            self.user_id = user_id
            data: tuple = (
                self.contract_id,
                self.name,
                self.final_client,
                self.client_project_code,
                self.start_date,
                self.end_date,
                self.price,
                self.currency,
                self.measurement_unit,
                self.status,
                self.user_id,
            )
            try:
                res: sqlite3.Cursor = db.execute_query(query=query, params=data)
                self.id = res.lastrowid
                return self
            except sqlite3.Error as e:
                raise HTTPException(500, e.args[0])

    def update(self, client_id: int, contract_id: int, work_order_id: int, user_id: int):
        permitted_action: bool = check_permissions(
            client_id=client_id, current_user_id=user_id, contract_id=contract_id, wo_id=work_order_id
        )
        if permitted_action:
            query = "UPDATE work_orders SET name = ?, final_client = ?, client_project_code = ?, start_date = ?, end_date = ?, price = ?, currency = ?, measurement_unit = ?, status = ? WHERE id == ? AND contract_id == ? AND user_id == ?"
            self.id = work_order_id
            self.contract_id = contract_id
            self.user_id = user_id
            data = (
                self.name,
                self.final_client,
                self.client_project_code,
                self.start_date,
                self.end_date,
                self.price,
                self.currency,
                self.measurement_unit,
                self.status,
                self.id,
                self.contract_id,
                self.user_id,
            )
            try:
                _: sqlite3.Cursor = db.execute_query(query=query, params=data)
                updated_work_order: WorkOrder = show_work_order(
                    work_order_id=self.id, contract_id=self.contract_id, user_id=self.user_id, client_id=client_id
                )
                return updated_work_order
            except sqlite3.Error as e:
                raise HTTPException(500, e.args[0])


def show_work_order(client_id: int, contract_id: int, work_order_id: int, user_id: int):
    permitted_action: bool = check_permissions(
        client_id=client_id, contract_id=contract_id, current_user_id=user_id, wo_id=work_order_id
    )
    if permitted_action:
        query = "SELECT * FROM work_orders WHERE id == ? AND contract_id == ? AND user_id == ?"
        data = (work_order_id, contract_id, user_id)
        try:
            res: sqlite3.Cursor = db.execute_query(query=query, params=data)
            row: tuple = res.fetchone()
            if row:
                work_order: WorkOrder = WorkOrder(
                    id=int(row[0]),
                    contract_id=row[1],
                    name=row[2],
                    final_client=row[3],
                    client_project_code=row[4],
                    start_date=row[5],
                    end_date=row[6],
                    price=row[7],
                    currency=row[8],
                    measurement_unit=row[9],
                    status=row[10],
                    user_id=row[11],
                )
                return work_order
            else:
                raise HTTPException(404, "No such work order")
        except sqlite3.Error as e:
            raise HTTPException(500, e.args[0])


def list_work_orders(client_id: int,contract_id: int, user_id: int):
    permitted_action: bool = check_permissions(
            client_id=client_id, contract_id=contract_id, current_user_id=user_id
        )
    if permitted_action:
        work_order_list: list[WorkOrder] = []
        query = "SELECT * FROM work_orders WHERE contract_id == ? AND user_id == ?"
        data: tuple = (contract_id, user_id)
        try:
            res: sqlite3.Cursor = db.execute_query(query=query, params=data)
            rows: list[tuple] = res.fetchall()
            for row in rows:
                work_order: WorkOrder = WorkOrder(
                    id=int(row[0]),
                    contract_id=row[1],
                    name=row[2],
                    final_client=row[3],
                    client_project_code=row[4],
                    start_date=row[5],
                    end_date=row[6],
                    price=row[7],
                    currency=row[8],
                    measurement_unit=row[9],
                    status=row[10],
                    user_id=row[11],
                )
                work_order_list.append(work_order)
            return work_order_list
        except sqlite3.OperationalError as e:
            raise HTTPException(500, e.args[0])


def delete_user_work_order(client_id: int,contract_id: int, work_order_id: int, user_id: int):
    permitted_action: bool = check_permissions(
        client_id=client_id, wo_id=work_order_id, current_user_id=user_id, contract_id=contract_id
    )
    if permitted_action:
        query = "DELETE FROM work_orders WHERE id == ? AND contract_id == ? AND user_id == ?"
        data = (work_order_id, contract_id, user_id)
        try:
            checkout_wo: WorkOrder = show_work_order(
                client_id=client_id, contract_id=contract_id, work_order_id=work_order_id, user_id=user_id
            )
            if type(checkout_wo) is WorkOrder:
                _: sqlite3.Cursor = db.execute_query(query=query, params=data)
                return True
            else:
                raise HTTPException(404, "No such work_order")
        except sqlite3.IntegrityError as e:
            raise HTTPException(500, e.args[0])


def check_permissions(
    client_id: int, current_user_id: int, contract_id: int, wo_id: int | None = None
):
    if wo_id:
        query = """SELECT wo.user_id
            FROM work_orders AS wo
            JOIN contracts AS ctr on wo.contract_id = ctr.id
            JOIN clients AS cli on ctr.client_id = cli.id
            WHERE ctr.id = ? AND cli.id = ? AND wo.id = ?"""
        data = (contract_id, client_id, wo_id)
    else:
        query = """SELECT ctr.user_id
            FROM contracts AS ctr
            JOIN clients AS cli on ctr.client_id = cli.id
            WHERE ctr.id = ? AND cli.id = ?"""
        data = (contract_id, client_id)
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
        raise HTTPException(500, e.args[0])
    if retrieved_user_id == current_user_id:
        return True
    else:
        raise HTTPException(
            status_code=403, detail="You are not allowed to perform this action"
        )
