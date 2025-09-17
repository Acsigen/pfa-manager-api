package models

import "github.com/Acsigen/pfa-manager-api/database"

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
