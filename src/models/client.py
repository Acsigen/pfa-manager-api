from pydantic import BaseModel
from fastapi import HTTPException
import sqlite3 # For error handling
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
    user_id: int | None = None

    def add(self):
        query = "INSERT INTO clients(name, address, contact_person, country, phone_number, onrc_no, cui, user_id) VALUES (?,?,?,?,?,?,?,?)"
        self.user_id = 0
        data = (self.name, self.address, self.contact_person, self.country, self.phone_number, self.onrc_no, self.cui, self.user_id)
        try: 
            res: sqlite3.Cursor = db.execute_query(query=query, params=data)
            self.id = res.lastrowid
            return self
        except sqlite3.IntegrityError as e:
            raise HTTPException(500,e.args[0])

    def update(self, client_id, user_id):
        query = "UPDATE clients	SET name = ?, address = ?, contact_person = ?, country = ?, phone_number = ?, onrc_no = ?, cui = ?	WHERE id = ?"
        self.user_id = user_id
        self.id = client_id
        data = (self.name, self.address, self.contact_person, self.country, self.phone_number, self.onrc_no, self.cui, self.id)
        try: 
            _: sqlite3.Cursor = db.execute_query(query=query, params=data)
            return self
        except sqlite3.IntegrityError as e:
            raise HTTPException(500,e.args[0])
    
def show_client(client_id: int):
    query = "SELECT * FROM clients WHERE id == ?"
    data = (client_id,)
    try: 
        res: sqlite3.Cursor = db.execute_query(query=query, params=data)
        row: tuple = res.fetchone()
        client: Client = Client(id=int(row[0]),
                        name=row[1],
                        address=row[2],
                        contact_person=row[3],
                        country=row[4],
                        phone_number=row[5],
                        onrc_no=row[6],
                        cui=row[7],
                        user_id=int(row[8])
        )
        return client
    except sqlite3.IntegrityError as e:
        raise HTTPException(500,e.args[0])

def list_clients():
    client_list: list[Client] = []
    query = "SELECT * FROM clients"
    try: 
        res: sqlite3.Cursor = db.execute_query(query=query)
        rows: list[tuple] = res.fetchall()
        for row in rows:
            client: Client = Client(id=int(row[0]),
                            name=row[1],
                            address=row[2],
                            contact_person=row[3],
                            country=row[4],
                            phone_number=row[5],
                            onrc_no=row[6],
                            cui=row[7],
                            user_id=int(row[8]))
            client_list.append(client)
        return client_list
    except sqlite3.OperationalError as e:
        raise HTTPException(500,e.args[0])

def delete_client(client_id: int):
    query = "DELETE FROM clients WHERE id == ?"
    data = (client_id,)
    try: 
        _: sqlite3.Cursor = db.execute_query(query=query, params=data)
        return True
    except sqlite3.IntegrityError as e:
        raise HTTPException(500,e.args[0])

