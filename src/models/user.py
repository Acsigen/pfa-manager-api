from pydantic import BaseModel
from fastapi import HTTPException
import sqlite3 # For error handling
from ..database import db
from ..utils.hash import hash_password, verify_password

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

def authenticate_user(username: str, password: str):
    email_address = username
    password = password
    query = "SELECT id,password FROM users where email_address == ?"
    data = (email_address,)
    try:
        res: sqlite3.Cursor = db.execute_query(query=query, params=data)
        retrieved_data: tuple = res.fetchone()
        # TODO: Check if the retrieved data returns something to treat the error where the email address is not in the db
        check_credentials: bool = verify_password(password=password, stored=retrieved_data[1])
        if check_credentials:
            user_id: int = retrieved_data[0]
            return user_id
        else:
            raise HTTPException(401,"Invalid credentials")
    except sqlite3.Error as e:
        raise HTTPException(500, e.args[0])

