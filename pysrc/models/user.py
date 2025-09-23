from pydantic import BaseModel
from fastapi import HTTPException
import sqlite3 # For error handling
from ..database import db
from ..utils.hash import hash_password

class User(BaseModel):
    id: int | None = None
    first_name: str
    last_name: str
    phone_number: str | None = None
    email_address: str
    password: str

    def add(self):
        query = "INSERT INTO users(first_name, last_name, phone_number, email_address, password) VALUES (?, ?, ?, ?, ?)"
        self.password = hash_password(password=self.password)
        data = (self.first_name, self.last_name, self.phone_number, self.email_address, self.password)
        try:
            res: sqlite3.Cursor = db.execute_query(query=query, params=data)
            self.id = res.lastrowid
            self.password = "REDACTED"
            return self
        except sqlite3.Error as e:
            raise HTTPException(500, e.args[0])
