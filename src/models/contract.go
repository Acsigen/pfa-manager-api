package models

import (
	"github.com/Acsigen/pfa-manager-api/database"
)

// Contract model, used tags to set the required items
type Contract struct {
	ID              int64
	UserID          int64
	ClientID        int64
	ContractNo      string `binding:"required"`
	StartDate       string `binding:"required"`
	EndDate         string `binding:"required"`
	Description     string
	CloudStorageUrl string
}

// Add a new contract
func (ctr *Contract) Add() error {
	// Build the query, use ? to avoid SQL injection
	query := `INSERT INTO contracts(contract_no, client_id, start_date, end_date, description, cloud_storage_url, user_id)
	VALUES (?,?,?,?,?,?,?)`

	// Prepare the query
	statement, err := database.DB.Prepare(query)
	if err != nil {
		return err
	}

	// Close the statement when the function call ends
	defer statement.Close()

	// Execute the query
	res, err := statement.Exec(ctr.ContractNo, ctr.ClientID, ctr.StartDate, ctr.EndDate, ctr.Description, ctr.CloudStorageUrl, ctr.UserID)
	if err != nil {
		return err
	}

	// Get the last insterted ID
	id, err := res.LastInsertId()

	// Set the ID of the client object so we can return it with the object in another function
	ctr.ID = id
	return err
}

// Method for updating a contract
func (ctr *Contract) Update() error {
	// Build the query, use ? to avoid SQL injection
	query := `UPDATE contracts
	SET contract_no = ?, start_date = ?, end_date = ?, description = ?, cloud_storage_url = ?
	WHERE id == ?`

	// Prepare the query
	statement, err := database.DB.Prepare(query)
	if err != nil {
		return err
	}

	// Close the statement when the function call ends
	defer statement.Close()

	// Execute the query
	_, err = statement.Exec(ctr.ContractNo, ctr.StartDate, ctr.EndDate, ctr.Description, ctr.CloudStorageUrl, ctr.ID)
	return err
}

// Function to get the list of contracts, return a list of contracts and error type
// This is not required to be a method since we don't really use the struct to insert data, we just create a list of contracts
func GetContractsList(userId int64, clientId int64) ([]Contract, error) {
	// Build the query
	query := "SELECT * FROM contracts where user_id == ? AND client_id == ?"

	// Direclty execute the query
	rows, err := database.DB.Query(query, userId, clientId)
	if err != nil {
		return nil, err
	}

	// Close the database connection when function call is done
	defer rows.Close()

	// Create the data structure for the return
	var contracts []Contract

	// Iterate over each row
	for rows.Next() {
		// Scan each row and map the items to client properties
		// The order of the arguments for the Scan function must be the same as the DB table not the model
		var contract Contract
		err := rows.Scan(&contract.ID,
			&contract.ContractNo,
			&contract.ClientID,
			&contract.StartDate,
			&contract.EndDate,
			&contract.Description,
			&contract.CloudStorageUrl,
			&contract.UserID)
		if err != nil {
			return nil, err
		}

		// append each client to the list of clients
		contracts = append(contracts, contract)
	}

	// Return the clients and no error
	return contracts, nil
}

// Function to retrieve the client with a specific ID
// This is not required to be a method since we don't really use the struct to insert data, we just retrieve a client from DB
func GetContractById(id int64) (*Contract, error) {
	// We build the query this way to avoid SQL injection
	query := "SELECT * FROM contracts WHERE id == ?"
	row := database.DB.QueryRow(query, id)

	// Scan the row and map the items to client properties
	var contract Contract
	err := row.Scan(&contract.ID,
		&contract.ContractNo,
		&contract.ClientID,
		&contract.StartDate,
		&contract.EndDate,
		&contract.Description,
		&contract.CloudStorageUrl,
		&contract.UserID)
	if err != nil {
		return nil, err
	}

	// Return the client
	return &contract, nil
}

// Method to delete a contract
func (c Contract) Delete(id int64) error {
	// Query statement
	query := "DELETE FROM contracts WHERE id == ?"
	statement, err := database.DB.Prepare(query)
	if err != nil {
		return err
	}

	// Close the statement when optimal
	defer statement.Close()

	// execute the query with the id of the contract
	_, err = statement.Exec(id)

	return err
}
