import sqlite3

class DB():
    try:
        con = sqlite3.connect("./data/tutorial.db")
        cursor = con.cursor()
    except sqlite3.Error as e:
        print(e)
        exit(1)

def create_tables(db: sqlite3.Cursor):
    tables = [
        {
            "table_name": "users",
            "query":"""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                email_address TEXT NOT NULL,
                password TEXT NOT NULL,
                UNIQUE(email_address, phone_number)
            )
            """
        },
        {
            "table_name": "clients",
            "query":"""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                contact_person TEXT NOT NULL,
                country TEXT NOT NULL,
                phone_number TEXT,
                onrc_no TEXT NOT NULL,
                cui TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                UNIQUE(onrc_no,cui),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        }
    ]
    
    for table in tables:
        try:
            db.execute(table['query'])
            print(f"Created {table['table_name']} table")
        except Exception as e:
            print(e)
            exit(1)

def init_db():
    db = DB
    create_tables(db.cursor)
