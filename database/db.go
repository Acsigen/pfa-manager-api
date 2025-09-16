package database

// When adding _ before the import url, we tell the compiler not to remove it
// Since we do not use the driver directly, the compiler would remove it
import (
	"database/sql"

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

	// Run the queries
	_, err := DB.Exec(createUsersTable)
	if err != nil {
		panic("Could not create users table.")
	}
	_, err = DB.Exec(createClientsTable)
	if err != nil {
		panic("Could not create clients table.")
	}
}
