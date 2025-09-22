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
    phone_number: int | None = None
    onrc_no: str
    cui: str
    user_id: int | None = None

    def create_client(self):
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
