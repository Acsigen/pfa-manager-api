from pydantic import BaseModel
from fastapi import HTTPException
import sqlite3
from ..database import db

NOT_FOUND_ERR: str = "No such contract"

class Contract(BaseModel):
    id: int | None = None
    contract_no: str
    start_date: str
    end_date: str
    description: str | None = None
    cloud_storage_url: str | None = None
    client_id: int | None = 0
    user_id: int | None = 0

    def add(self, client_id, user_id: int):
        permitted_action: bool = check_permissions(
            client_id=client_id, current_user_id=user_id
        )
        if permitted_action:
            query = "INSERT INTO contracts(contract_no, start_date, end_date, description, cloud_storage_url, client_id, user_id) VALUES (?,?,?,?,?,?,?)"
            self.client_id = client_id
            self.user_id = user_id
            data: tuple = (
                self.contract_no,
                self.start_date,
                self.end_date,
                self.description,
                self.cloud_storage_url,
                self.client_id,
                self.user_id,
            )
            try:
                res: sqlite3.Cursor = db.execute_query(query=query, params=data)
                self.id = res.lastrowid
                return self
            except sqlite3.IntegrityError as e:
                raise HTTPException(500, e.args[0])

    def update(self, contract_id: int, client_id: int, user_id: int):
        permitted_action: bool = check_permissions(
            client_id=client_id, current_user_id=user_id, contract_id=contract_id
        )
        if permitted_action:
            query = "UPDATE contracts SET contract_no = ?, start_date = ?, end_date = ?, description = ?, cloud_storage_url = ? WHERE id = ? AND client_id == ? AND user_id == ?"
            self.id = contract_id
            self.client_id = client_id
            self.user_id = user_id
            data = (
                self.contract_no,
                self.start_date,
                self.end_date,
                self.description,
                self.cloud_storage_url,
                self.id,
                self.client_id,
                self.user_id,
            )
            try:
                checkout_contract: Contract = show_contract(
                    contract_id=contract_id, client_id=client_id, user_id=user_id
                )
                if type(checkout_contract) is Contract:
                    _: sqlite3.Cursor = db.execute_query(query=query, params=data)
                    return self
                else:
                    raise HTTPException(404, NOT_FOUND_ERR)
            except sqlite3.IntegrityError as e:
                raise HTTPException(500, e.args[0])


def show_contract(contract_id: int, client_id: int, user_id: int):
    permitted_action: bool = check_permissions(
        client_id=client_id, current_user_id=user_id, contract_id=contract_id
    )
    if permitted_action:
        query = (
            "SELECT * FROM contracts WHERE id == ? AND client_id == ? AND user_id == ?"
        )
        data = (contract_id, client_id, user_id)
        try:
            res: sqlite3.Cursor = db.execute_query(query=query, params=data)
            row: tuple = res.fetchone()
            if row:
                print(row)
                contract: Contract = Contract(
                    id=int(row[0]),
                    contract_no=row[1],
                    start_date=row[2],
                    end_date=row[3],
                    description=row[4],
                    cloud_storage_url=row[5],
                    client_id=row[6],
                    user_id=row[7],
                )
                return contract
            else:
                raise HTTPException(404, NOT_FOUND_ERR)
        except sqlite3.Error as e:
            raise HTTPException(500, e.args[0])


def list_user_contracts(client_id: int, user_id: int):
    permitted_action: bool = check_permissions(
        client_id=client_id, current_user_id=user_id
    )
    if permitted_action:
        contract_list: list[Contract] = []
        query = "SELECT * FROM contracts WHERE client_id == ? AND user_id == ?"
        data: tuple = (client_id, user_id)
        try:
            res: sqlite3.Cursor = db.execute_query(query=query, params=data)
            rows: list[tuple] = res.fetchall()
            for row in rows:
                contract: Contract = Contract(
                    id=int(row[0]),
                    contract_no=row[1],
                    start_date=row[2],
                    end_date=row[3],
                    description=row[4],
                    cloud_storage_url=row[5],
                    client_id=row[6],
                    user_id=row[7],
                )
                contract_list.append(contract)
            return contract_list
        except sqlite3.OperationalError as e:
            raise HTTPException(500, e.args[0])


def delete_user_contract(contract_id: int, client_id: int, user_id: int):
    permitted_action: bool = check_permissions(
        client_id=client_id, current_user_id=user_id, contract_id=contract_id
    )
    if permitted_action:
        query = (
            "DELETE FROM contracts WHERE id == ? AND client_id == ? AND user_id == ?"
        )
        data = (contract_id, client_id, user_id)
        try:
            checkout_contract = show_contract(
                contract_id=contract_id, client_id=client_id, user_id=user_id
            )
            if type(checkout_contract) is Contract:
                _: sqlite3.Cursor = db.execute_query(query=query, params=data)
                return True
            else:
                raise HTTPException(404, NOT_FOUND_ERR)
        except sqlite3.IntegrityError as e:
            raise HTTPException(500, e.args[0])


def check_permissions(
    client_id: int, current_user_id: int, contract_id: int | None = None
):
    if contract_id:
        query = """SELECT ctr.user_id
            FROM contracts AS ctr
            JOIN clients AS cli on ctr.client_id = cli.id
            WHERE ctr.id = ? AND cli.id = ?"""
        data = (contract_id, client_id)
    else:
        query = "SELECT user_id FROM clients WHERE id == ?"
        data = (client_id,)
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
