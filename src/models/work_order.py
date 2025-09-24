from pydantic import BaseModel
from fastapi import HTTPException
import sqlite3 # For error handling
from ..database import db
from .client import check_user_id

class WorkOrder(BaseModel):
    id:  int | None = None
    contract_id:  int | None = None
    name: str
    final_client: str
    client_project_code: str | None = "N/A"
    start_date: str
    end_date: str
    price: float
    currency: str
    measurement_unit: str
    status: str | None = None

    def add(self, contract_id: int, user_id: int, client_id: int):
        check_permissions: bool = check_user_id(client_id=client_id, user_id=user_id)
        if check_permissions:
            query = "INSERT INTO work_orders(contract_id, name, final_client, client_project_code, start_date, end_date, price, currency, measurement_unit, status) VALUES (?,?,?,?,?,?,?,?,?,?)"
            self.contract_id = contract_id
            data: tuple = (self.contract_id, self.name, self.final_client, self.client_project_code,self.start_date,self.end_date,self.price,self.currency,self.measurement_unit,self.status)
            try: 
                res: sqlite3.Cursor = db.execute_query(query=query, params=data)
                self.id = res.lastrowid
                return self
            except sqlite3.Error as e:
                raise HTTPException(500,e.args[0])

    def update(self, contract_id, work_order_id):
        query = "UPDATE work_orders SET name = ?, final_client = ?, client_project_code = ?, start_date = ?, end_date = ?, price = ?, currency = ?, measurement_unit = ?, status = ? WHERE id == ? AND contract_id == ?"
        self.id = work_order_id
        self.contract_id = contract_id
        data = (self.name,self.final_client,self.client_project_code,self.start_date,self.end_date,self.price,self.currency,self.measurement_unit,self.status, self.id, self.contract_id)
        try: 
            _: sqlite3.Cursor = db.execute_query(query=query, params=data)
            updated_work_order: WorkOrder = show_work_order(work_order_id=self.id,contract_id=self.contract_id)
            return updated_work_order
        except sqlite3.Error as e:
            raise HTTPException(500,e.args[0])

def show_work_order(contract_id: int, work_order_id: int):
    query = "SELECT * FROM work_orders WHERE id == ? AND contract_id == ?"
    data = (work_order_id,contract_id)
    try: 
        res: sqlite3.Cursor = db.execute_query(query=query, params=data)
        row: tuple = res.fetchone()
        if row:
            print(row)
            work_order: WorkOrder = WorkOrder(id=int(row[0]),
                            contract_id=row[1],
                            name=row[2],
                            final_client=row[3],
                            client_project_code=row[4],
                            start_date=row[5],
                            end_date=row[6],
                            price=row[7],
                            currency=row[8],
                            measurement_unit=row[9],
                            status=row[10]
            )
            return work_order
        else:
            raise HTTPException(404, "No such work order")
    except sqlite3.Error as e:
        raise HTTPException(500,e.args[0])

def list_work_orders(contract_id: int):
    work_order_list: list[WorkOrder] = []
    query = "SELECT * FROM work_orders WHERE contract_id == ?"
    data: tuple = (contract_id,)
    try: 
        res: sqlite3.Cursor = db.execute_query(query=query, params=data)
        rows: list[tuple] = res.fetchall()
        for row in rows:
            work_order: WorkOrder = WorkOrder(id=int(row[0]),
                            contract_id=row[1],
                            name=row[2],
                            final_client=row[3],
                            client_project_code=row[4],
                            start_date=row[5],
                            end_date=row[6],
                            price=row[7],
                            currency=row[8],
                            measurement_unit=row[9],
                            status=row[10])
            work_order_list.append(work_order)
        return work_order_list
    except sqlite3.OperationalError as e:
        raise HTTPException(500,e.args[0])

def delete_work_order(contract_id: int, work_order_id: int):
    query = "DELETE FROM work_orders WHERE id == ? AND contract_id == ?"
    data = (work_order_id,contract_id)
    try: 
        checkout_wo = show_work_order(contract_id=contract_id, work_order_id=work_order_id)
        if type(checkout_wo) is WorkOrder:
            _: sqlite3.Cursor = db.execute_query(query=query, params=data)
            return True
        else:
            raise HTTPException(404, "No such work_order")
    except sqlite3.IntegrityError as e:
        raise HTTPException(500,e.args[0])