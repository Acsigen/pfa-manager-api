from fastapi import HTTPException
import sqlite3  # For error handling
from ..database import db

ALLOWED_TABLES: list = [
    "clients",
    "contracts",
    "work_orders",
    "activity_reports",
    "invoices",
]

def check_permissions(current_user_id: int, item_id: int, table_name: str):
    if table_name not in ALLOWED_TABLES:
        raise HTTPException(status_code=403, detail="Bad query data")
    else:
        query = f"SELECT user_id FROM {table_name} WHERE id == ?"
        data = (item_id,)
        try:
            res: sqlite3.Cursor = db.execute_query(query=query, params=data)
            row: tuple = res.fetchone()
            if row:
                item_user_id: int = int(row[0])
            else:
                raise HTTPException(status_code=404, detail="Not found")
        except sqlite3.Error as e:
            raise HTTPException(500, e.args[0])
        if item_user_id == current_user_id:
            return True
        else:
            raise HTTPException(
                status_code=403, detail="You are not allowed to perform this action"
            )
