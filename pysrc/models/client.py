from pydantic import BaseModel
from fastapi import HTTPException
import sqlite3 # For error handling
from database.db import DB

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
        db = DB
        query = "INSERT INTO clients(name, address, contact_person, country, phone_number, onrc_no, cui, user_id) VALUES (?,?,?,?,?,?,?,?)"
        self.user_id = 0
        data = (self.name, self.address, self.contact_person, self.country, self.phone_number, self.onrc_no, self.cui, self.user_id)
        try: 
            db.cursor.execute(query, data)
            self.id = db.cursor.lastrowid
            db.con.commit()
            raise HTTPException(201,self.__dict__)
        except sqlite3.IntegrityError as e:
            raise HTTPException(500,e.args[0])

    def update(self, client_id):
        db = DB
        query = "UPDATE clients	SET name = ?, address = ?, contact_person = ?, country = ?, phone_number = ?, onrc_no = ?, cui = ?	WHERE id = ?"
        self.user_id = 0
        self.id = client_id
        data = (self.name, self.address, self.contact_person, self.country, self.phone_number, self.onrc_no, self.cui, self.id)
        try: 
            db.cursor.execute(query, data)
            db.con.commit()
            return self
        except sqlite3.IntegrityError as e:
            raise HTTPException(500,e.args[0])
    
def show_client(client_id: int):
    db = DB
    query = "SELECT * FROM clients WHERE id == ?"
    data = (client_id,)
    try: 
        db.cursor.execute(query, data)
        res = db.cursor.fetchone()
        client = Client(id=int(res[0]),
                        name=res[1],
                        address=res[2],
                        contact_person=res[3],
                        country=res[4],
                        phone_number=res[5],
                        onrc_no=res[6],
                        cui=res[7],
                        user_id=int(res[8])
        )
        return client
    except sqlite3.IntegrityError as e:
        raise HTTPException(500,e.args[0])

def list_clients():
    db = DB
    client_list = []
    query = "SELECT * FROM clients"
    try: 
        db.cursor.execute(query)
        res = db.cursor.fetchall()
        for row in res:
            client = Client(id=int(row[0]),
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
        return e.args[0]

def delete_client(client_id: int):
    db = DB
    query = "DELETE FROM clients WHERE id == ?"
    data = (client_id,)
    try: 
        db.cursor.execute(query, data)
        db.con.commit()
        raise HTTPException(201,"Client deleted")
    except sqlite3.IntegrityError as e:
        raise HTTPException(500,e.args[0])

