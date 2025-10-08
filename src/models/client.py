from pydantic import BaseModel
from fastapi import HTTPException
import sqlite3  # For error handling
from ..database import db


class Client(BaseModel):
    id: int | None = None
    name: str
    address: str
    contact_person: str
    country: str
    phone_number: str | None = None
    onrc_no: str
    cui: str
    pv_sign_template: str | None
    wo_sign_template: str | None
    user_id: int | None = None

    def add(self, user_id: int):
        query = "INSERT INTO clients(name, address, contact_person, country, phone_number, onrc_no, cui, pv_sign_template, wo_sign_template, user_id) VALUES (?,?,?,?,?,?,?,?,?,?)"
        self.user_id = user_id
        data = (
            self.name,
            self.address,
            self.contact_person,
            self.country,
            self.phone_number,
            self.onrc_no,
            self.cui,
            self.pv_sign_template,
            self.wo_sign_template,
            self.user_id,
        )
        try:
            res: sqlite3.Cursor = db.execute_query(query=query, params=data)
            self.id = res.lastrowid
            return self
        except sqlite3.IntegrityError as e:
            raise HTTPException(500, e.args[0])

    def update(self, client_id: int, user_id: int):
        permitted_action: bool = check_permissions(
            client_id=client_id, current_user_id=user_id
        )
        if permitted_action:
            query = "UPDATE clients	SET name = ?, address = ?, contact_person = ?, country = ?, phone_number = ?, onrc_no = ?, cui = ?, pv_sign_template = ?, wo_sign_template = ? WHERE id == ? AND user_id == ?"
            self.user_id = user_id
            self.id = client_id
            data = (
                self.name,
                self.address,
                self.contact_person,
                self.country,
                self.phone_number,
                self.onrc_no,
                self.cui,
                self.pv_sign_template,
                self.wo_sign_template,
                self.id,
                self.user_id,
            )
            try:
                _: sqlite3.Cursor = db.execute_query(query=query, params=data)
                return self
            except sqlite3.IntegrityError as e:
                raise HTTPException(500, e.args[0])


def show_user_client(client_id: int, user_id: int):
    permitted_action: bool = check_permissions(
        client_id=client_id, current_user_id=user_id
    )
    if permitted_action:
        query = "SELECT * FROM clients WHERE id == ? AND user_id == ?"
        data = (client_id, user_id)
        try:
            res: sqlite3.Cursor = db.execute_query(query=query, params=data)
            row: tuple = res.fetchone()
            client: Client = Client(
                id=int(row[0]),
                name=row[1],
                address=row[2],
                contact_person=row[3],
                country=row[4],
                phone_number=row[5],
                onrc_no=row[6],
                cui=row[7],
                pv_sign_template=row[8],
                wo_sign_template=row[9],
                user_id=int(row[10]),
            )
            return client
        except sqlite3.IntegrityError as e:
            raise HTTPException(500, e.args[0])


def list_user_clients(user_id: int):
    client_list: list[Client] = []
    query = "SELECT * FROM clients where user_id == ?"
    data = (user_id,)
    try:
        res: sqlite3.Cursor = db.execute_query(query=query, params=data)
        rows: list[tuple] = res.fetchall()
        for row in rows:
            client: Client = Client(
                id=int(row[0]),
                name=row[1],
                address=row[2],
                contact_person=row[3],
                country=row[4],
                phone_number=row[5],
                onrc_no=row[6],
                cui=row[7],
                pv_sign_template=row[8],
                wo_sign_template=row[9],
                user_id=int(row[10]),
            )
            client_list.append(client)
        return client_list
    except sqlite3.OperationalError as e:
        raise HTTPException(500, e.args[0])


def delete_client(client_id: int, user_id: int):
    permitted_action: bool = check_permissions(
        client_id=client_id, current_user_id=user_id
    )
    if permitted_action:
        query = "DELETE FROM clients WHERE id == ? AND user_id == ?"
        data = (client_id, user_id)
        try:
            _: sqlite3.Cursor = db.execute_query(query=query, params=data)
            return True
        except sqlite3.IntegrityError as e:
            raise HTTPException(500, e.args[0])


def check_permissions(current_user_id: int, client_id: int):
    query = "SELECT user_id FROM clients WHERE id == ?"
    data = (client_id,)
    try:
        res: sqlite3.Cursor = db.execute_query(query=query, params=data)
        row: tuple = res.fetchone()
        if row:
            item_user_id: int = int(row[0])
        else:
            raise HTTPException(status_code=404, detail="No such client")
    except sqlite3.Error as e:
        raise HTTPException(500, e.args[0])
    if item_user_id == current_user_id:
        return True
    else:
        raise HTTPException(
            status_code=403, detail="You are not allowed to perform this action"
        )
