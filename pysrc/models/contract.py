from pydantic import BaseModel
from fastapi import HTTPException
import sqlite3 # For error handling
from ..database import db

class Contract(BaseModel):
    id: int | None = None
    contract_no: str
    start_date: str
    end_date: str
    description: str | None = None
    cloud_storage_url: str | None = None
    client_id: int | None = 0


    def add(self, client_id):
        query = "INSERT INTO contracts(contract_no, start_date, end_date, description, cloud_storage_url, client_id) VALUES (?,?,?,?,?,?)"
        self.client_id = client_id
        data: tuple = (self.contract_no, self.start_date, self.end_date, self.description, self.cloud_storage_url, self.client_id)
        try: 
            res: sqlite3.Cursor = db.execute_query(query=query, params=data)
            self.id = res.lastrowid
            return self
        except sqlite3.IntegrityError as e:
            raise HTTPException(500,e.args[0])

def show_contract(contract_id: int):
    query = "SELECT * FROM contracts WHERE id == ?"
    data = (contract_id,)
    try: 
        res: sqlite3.Cursor = db.execute_query(query=query, params=data)
        row: tuple = res.fetchone()
        contract: Contract = Contract(id=int(row[0]),
                        contract_no=row[1],
                        start_date=row[2],
                        end_date=row[3],
                        description=row[4],
                        cloud_storage_url=row[5],
                        client_id=row[6]
        )
        return contract
    except sqlite3.IntegrityError as e:
        raise HTTPException(500,e.args[0])

# def list_clients():
#     client_list: list[Client] = []
#     query = "SELECT * FROM clients"
#     try: 
#         res: sqlite3.Cursor = db.execute_query(query=query)
#         rows: list[tuple] = res.fetchall()
#         for row in rows:
#             client: Client = Client(id=int(row[0]),
#                             name=row[1],
#                             address=row[2],
#                             contact_person=row[3],
#                             country=row[4],
#                             phone_number=row[5],
#                             onrc_no=row[6],
#                             cui=row[7],
#                             user_id=int(row[8]))
#             client_list.append(client)
#         return client_list
#     except sqlite3.OperationalError as e:
#         raise HTTPException(500,e.args[0])

# def delete_client(client_id: int):
#     query = "DELETE FROM clients WHERE id == ?"
#     data = (client_id,)
#     try: 
#         _: sqlite3.Cursor = db.execute_query(query=query, params=data)
#         return True
#     except sqlite3.IntegrityError as e:
#         raise HTTPException(500,e.args[0])