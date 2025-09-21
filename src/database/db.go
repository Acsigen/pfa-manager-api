package database

// When adding _ before the import url, we tell the compiler not to remove it
// Since we do not use the driver directly, the compiler would remove it
import (
	"database/sql"
	"fmt"

	_ "github.com/mattn/go-sqlite3"
)

// Use this as a variable to directly access the connection from outside of the package
var DB *sql.DB

// Initialise the DB connection
func InitDB() {
	// Define the error var
	var err error

	// Open the database file
	DB, err = sql.Open("sqlite3", "./data/sqlite.db")
	if err != nil {
		panic("The database could not be accessed")
	}

	// Set some connection properties
	DB.SetMaxOpenConns(10)
	DB.SetMaxIdleConns(5)

	// Create the tables
	createTables()
}

// Create tables function
func createTables() {
	// Define the query to create the users table
	createUsersTable := `
	CREATE TABLE IF NOT EXISTS users (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		first_name TEXT NOT NULL,
		last_name TEXT NOT NULL,
		phone_number TEXT NOT NULL,
		email_address TEXT NOT NULL,
		password TEXT NOT NULL,
		UNIQUE(email_address, phone_number)
	)
	`
	// Define the query to create the clients table
	createClientsTable := `
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
	`

	// Define the query to create the contracts table
	createContractsTable := `
	CREATE TABLE IF NOT EXISTS contracts (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		contract_no TEXT NOT NULL,
		client_id integer NOT NULL,
		start_date TEXT NOT NULL,
		end_date TEXT NOT NULL,
		description TEXT,
		cloud_storage_url TEXT,
		user_id INTEGER NOT NULL,
		FOREIGN KEY(user_id) REFERENCES users(id),
		FOREIGN KEY(client_id) REFERENCES clients(id)
	)
	`

	// Define the query to create the work orders table
	createWoTable := `
	CREATE TABLE IF NOT EXISTS work_orders (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		user_id INTEGER NOT NULL,
		client_id INTEGER NOT NULL,
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
		FOREIGN KEY(user_id) REFERENCES users(id),
		FOREIGN KEY(client_id) REFERENCES clients(id),
		FOREIGN KEY(contract_id) REFERENCES contracts(id),
		UNIQUE(name)
	)
	`

	// Define the query to create the work orders table
	createArTable := `
	CREATE TABLE IF NOT EXISTS activity_reports (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		user_id INTEGER NOT NULL,
		client_id INTEGER NOT NULL,
		contract_id INTEGER NOT NULL,
		wo_id INTEGER NOT NULL,
		invoice_id INTEGER,
		name TEXT NOT NULL,
		date TEXT NOT NULL,
		hours_amount REAL NOT NULL,
		FOREIGN KEY(user_id) REFERENCES users(id),
		FOREIGN KEY(client_id) REFERENCES clients(id),
		FOREIGN KEY(contract_id) REFERENCES contracts(id),
		FOREIGN KEY(wo_id) REFERENCES work_orders(id),
		UNIQUE(name)
	)
	`

	// Run the queries
	_, err := DB.Exec(createUsersTable)
	if err != nil {
		panic("Could not create users table.")
	}
	fmt.Println("Created users table")

	_, err = DB.Exec(createClientsTable)
	if err != nil {
		panic("Could not create clients table.")
	}
	fmt.Println("Created clients table")

	_, err = DB.Exec(createContractsTable)
	if err != nil {
		panic("Could not create contracts table.")
	}
	fmt.Println("Created contracts table")

	_, err = DB.Exec(createWoTable)
	if err != nil {
		panic("Could not create work orders table.")
	}
	fmt.Println("Created work orders table")

	_, err = DB.Exec(createArTable)
	if err != nil {
		panic("Could not create activity reports table.")
	}
	fmt.Println("Created activity reports table")
}
