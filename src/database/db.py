import sqlite3
import os

DB_FILE = "./data/tutorial.db"

def init_db():
    """
    Initializes the database by creating tables.
    This function should be called once, e.g., on application startup.
    """
    # Create the 'data' directory if it doesn't exist
    os.makedirs(name=os.path.dirname(p=DB_FILE), exist_ok=True)
    
    try:
        with sqlite3.connect(database=DB_FILE) as con:
            cursor: sqlite3.Cursor = con.cursor()
            create_tables(cursor=cursor)
            print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Error initializing the database: {e}")
        raise

def get_db_connection():
    """
    Returns a new database connection object.
    It's the caller's responsibility to manage this connection.
    """
    return sqlite3.connect(database=DB_FILE)

def execute_query(query, params=None):
    """
    A helper function to execute a single query within a transaction.
    It automatically handles the connection and cursor.
    """
    try:
        with sqlite3.connect(database=DB_FILE) as con:
            cursor: sqlite3.Cursor = con.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            # The 'with' statement handles the commit
            return cursor
    except sqlite3.Error as e:
        print(f"Database error during query execution: {e.args[0]}")
        # The 'with' statement handles the rollback
        raise

def create_tables(cursor):
    # This function remains the same as in the previous example
    tables = [
        {
            "table_name": "users",
            "query": """
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
            "query": """
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
                UNIQUE(onrc_no, cui),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        },
        {
            "table_name": "contracts",
            "query": """
            CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                contract_no TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                description TEXT,
                cloud_storage_url TEXT,
                client_id integer NOT NULL,
                FOREIGN KEY(client_id) REFERENCES clients(id)
            )
            """
        },
        {
            "table_name": "work_orders",
            "query": """
            CREATE TABLE IF NOT EXISTS work_orders (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                contract_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                final_client TEXT NOT NULL,
                client_project_code TEXT,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                price REAL NOT NULL,
                currency TEXT NOT NULL,
                measurement_unit TEXT NOT NULL,
                status TEXT,
                FOREIGN KEY(contract_id) REFERENCES contracts(id),
                UNIQUE(name)
            )
            """
        },
        {
            "table_name": "activity_reports",
            "query": """
            CREATE TABLE IF NOT EXISTS activity_reports (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                wo_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                hours_amount REAL NOT NULL,
                FOREIGN KEY(wo_id) REFERENCES work_orders(id),
                UNIQUE(name)
            )
            """
        },
        {
            "table_name": "invoices",
            "query": """
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                client_id INTEGER NOT NULL,
                currency TEXT NOT NULL,
                exchange_rate REAL NOT NULL,
                invoice_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                status TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY(client_id) REFERENCES clients(id)
                FOREIGN KEY(user_id) REFERENCES users(id)
                UNIQUE(name)
            )
            """
        },
        {
            "table_name": "invoice_items",
            "query": """
            CREATE TABLE IF NOT EXISTS invoice_items (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                ar_id INTEGER NOT NULL,
                invoice_id INTEGER NOT NULL,
                FOREIGN KEY(ar_id) REFERENCES activity_reports(id)
                FOREIGN KEY(invoice_id) REFERENCES invoices(id)
            )
            """
        }
    ]

    for table in tables:
        try:
            cursor.execute(table['query'])
            print(f"Created {table['table_name']} table")
        except sqlite3.Error as e:
            print(f"Error creating {table['table_name']} table: {e}")
            raise
