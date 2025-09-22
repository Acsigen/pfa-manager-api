package models

import (
	"github.com/Acsigen/pfa-manager-api/database"
)

// Contract model, used tags to set the required items
type Invoice struct {
	ID           int64
	Name         string `binding:"required"`
	ClientID     int64
	Currency     string `binding:"required"`
	ExchangeRate float64
	InvoiceDate  string `binding:"required"`
	DueDate      string `binding:"required"`
	Status       string `binding:"required"`
	UserID       int64
}

// Add a new contract
func (inv *Invoice) Add() error {
	// Build the query, use ? to avoid SQL injection
	query := `INSERT INTO invoices(name, client_id, currency, exchange_rate, invoice_date, due_date, status, user_id)
	VALUES (?,?,?,?,?,?,?,?)`

	// Prepare the query
	statement, err := database.DB.Prepare(query)
	if err != nil {
		return err
	}

	// Close the statement when the function call ends
	defer statement.Close()

	// Execute the query
	res, err := statement.Exec(inv.Name, inv.ClientID, inv.Currency, inv.ExchangeRate, inv.InvoiceDate, inv.DueDate, inv.Status, inv.UserID)
	if err != nil {
		return err
	}

	// Get the last insterted ID
	id, err := res.LastInsertId()

	// Set the ID of the client object so we can return it with the object in another function
	inv.ID = id
	return err
}

// // Method for updating a contract
// func (ctr *Contract) Update() error {
// 	// Build the query, use ? to avoid SQL injection
// 	query := `UPDATE contracts
// 	SET contract_no = ?, start_date = ?, end_date = ?, description = ?, cloud_storage_url = ?
// 	WHERE id == ?`

// 	// Prepare the query
// 	statement, err := database.DB.Prepare(query)
// 	if err != nil {
// 		return err
// 	}

// 	// Close the statement when the function call ends
// 	defer statement.Close()

// 	// Execute the query
// 	_, err = statement.Exec(ctr.ContractNo, ctr.StartDate, ctr.EndDate, ctr.Description, ctr.CloudStorageUrl, ctr.ID)
// 	return err
// }

// Function to get the list of contracts, return a list of contracts and error type
// This is not required to be a method since we don't really use the struct to insert data, we just create a list of contracts
func GetInvoiceList(userId int64) ([]Invoice, error) {
	// Build the query
	query := "SELECT * FROM invoices where user_id == ?"

	// Direclty execute the query
	rows, err := database.DB.Query(query, userId)
	if err != nil {
		return nil, err
	}

	// Close the database connection when function call is done
	defer rows.Close()

	// Create the data structure for the return
	var invoices []Invoice

	// Iterate over each row
	for rows.Next() {
		// Scan each row and map the items to client properties
		// The order of the arguments for the Scan function must be the same as the DB table not the model
		var invoice Invoice
		err := rows.Scan(&invoice.ID, &invoice.Name, &invoice.ClientID, &invoice.Currency, &invoice.ExchangeRate, &invoice.InvoiceDate, &invoice.DueDate, &invoice.Status, &invoice.UserID)
		if err != nil {
			return nil, err
		}

		// append each client to the list of clients
		invoices = append(invoices, invoice)
	}

	// Return the clients and no error
	return invoices, nil
}

// // Function to retrieve the client with a specific ID
// // This is not required to be a method since we don't really use the struct to insert data, we just retrieve a client from DB
// func GetContractById(id int64) (*Contract, error) {
// 	// We build the query this way to avoid SQL injection
// 	query := "SELECT * FROM contracts WHERE id == ?"
// 	row := database.DB.QueryRow(query, id)

// 	// Scan the row and map the items to client properties
// 	var contract Contract
// 	err := row.Scan(&contract.ID,
// 		&contract.ContractNo,
// 		&contract.ClientID,
// 		&contract.StartDate,
// 		&contract.EndDate,
// 		&contract.Description,
// 		&contract.CloudStorageUrl,
// 		&contract.UserID)
// 	if err != nil {
// 		return nil, err
// 	}

// 	// Return the client
// 	return &contract, nil
// }

// // Method to delete a contract
// func (c Contract) Delete(id int64) error {
// 	// Query statement
// 	query := "DELETE FROM contracts WHERE id == ?"
// 	statement, err := database.DB.Prepare(query)
// 	if err != nil {
// 		return err
// 	}

// 	// Close the statement when optimal
// 	defer statement.Close()

// 	// execute the query with the id of the contract
// 	_, err = statement.Exec(id)

// 	return err
// }
