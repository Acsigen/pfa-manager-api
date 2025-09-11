import sqlite3
import os
from fastapi import HTTPException
# from models.Client import Client

class DBConnection():
    """
    A class to handle SQLite database connections and table initialization.
    """
    db_path: str

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.__initialise_database()
    
    def __db_connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
         # Set the row factory to sqlite3.Row. This allows us to access
        # data by column name instead of by index.
        conn.row_factory = sqlite3.Row
        return conn

    def __initialise_database(self):
        data_migrations_directory = "./database-migrations"
        migration_files = os.listdir(data_migrations_directory)
        with self.__db_connect() as con:
            cursor = con.cursor()
            for file in migration_files:
                with open(os.path.join(data_migrations_directory,file),"r") as f:
                    sql_statement = f.read()
                    cursor.execute(sql_statement)
            con.commit()

    def get_all_clients(self):
        try:
            with self.__db_connect() as con:
                client_list = []
                cursor = con.cursor()
                resp = cursor.execute('SELECT id,name FROM clients')
                rows = resp.fetchall()
                for row in rows:
                    client_list.append(dict(row))
                return client_list
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_client_by_id(self,client_id):
        try:
            with self.__db_connect() as con:
                cursor = con.cursor()
                resp = cursor.execute(f'SELECT * FROM clients WHERE id == {client_id}')
                row = resp.fetchone()
                return row
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_client_by_cui(self,client_cui):
        try:
            with self.__db_connect() as con:
                cursor = con.cursor()
                resp = cursor.execute(f'SELECT * FROM clients WHERE cui == {client_cui}')
                row = resp.fetchone()
                return row
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def add_client(self, request_body: dict):
        request_body.pop('id')
        columns = ', '.join(request_body.keys())
        placeholders = ', '.join(['?'] * len(request_body))
        try:
            with self.__db_connect() as con:
                cursor = con.cursor()
                add_client_sql = f"INSERT INTO clients ({columns}) VALUES ({placeholders})"
                cursor.execute(add_client_sql,list(request_body.values()))
                con.commit()
            raise HTTPException(status_code=201, detail=request_body)
        except sqlite3.IntegrityError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_client(self, request_body: dict):
        client_id = request_body['id']
        request_body.pop('id')
        update_data = []
        for k,v in request_body.items():
            update_data.append(f"{k}='{v}'")
        print(update_data)
        try:
            with self.__db_connect() as con:
                cursor = con.cursor()
                add_client_sql = f"UPDATE clients SET {','.join(update_data)} WHERE  id == {client_id}"
                print(add_client_sql)
                cursor.execute(add_client_sql)
                con.commit()
            raise HTTPException(status_code=201, detail=request_body)
        except sqlite3.IntegrityError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=str(e))