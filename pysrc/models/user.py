from pydantic import BaseModel
from fastapi import HTTPException
import sqlite3 # For error handling
from database.db import DB
from utils.hash import hash_password

class User(BaseModel):
    id: int | None = None
    first_name: str
    last_name: str
    phone_number: str | None = None
    email_address: str
    password: str

    def add(self):
        db = DB
        query = "INSERT INTO users(first_name, last_name, phone_number, email_address, password) VALUES (?, ?, ?, ?, ?)"
        self.password = hash_password(self.password)
        data = (self.first_name, self.last_name, self.phone_number, self.email_address, self.password)
        try: 
            db.cursor.execute(query, data)
            self.id = db.cursor.lastrowid
            db.con.commit()
            self.password = "REDACTED"
            return self
        except sqlite3.IntegrityError as e:
            raise HTTPException(500,e.args[0])
