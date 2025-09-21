package models

import "github.com/Acsigen/pfa-manager-api/database"

// Contract model, used tags to set the required items
type ActivityReport struct {
	ID          int64
	UserID      int64
	ClientID    int64
	ContractID  int64
	WorkOrderID int64
	InvoiceId   int64
	Name        string  `binding:"required"`
	Date        string  `binding:"required"`
	HoursAmount float64 `binding:"required"`
}

// Add a new contract
func (ar *ActivityReport) Add() error {
	// Build the query, use ? to avoid SQL injection
	query := `INSERT INTO activity_reports(user_id, client_id, contract_id, wo_id, invoice_id, name, date, hours_amount)
	VALUES (?,?,?,?,?,?,?,?)`

	// Prepare the query
	statement, err := database.DB.Prepare(query)
	if err != nil {
		return err
	}

	// Close the statement when the function call ends
	defer statement.Close()

	// Execute the query
	res, err := statement.Exec(ar.UserID, ar.ClientID, ar.ContractID, ar.WorkOrderID, ar.InvoiceId, ar.Name, ar.Date, ar.HoursAmount)
	if err != nil {
		return err
	}

	// Get the last insterted ID
	id, err := res.LastInsertId()

	// Set the ID of the client object so we can return it with the object in another function
	ar.ID = id
	return err
}

// Method for updating a contract
func (ar *ActivityReport) Update() error {
	// Build the query, use ? to avoid SQL injection
	// TODO: Change the invoice ID when invoice section is implemented
	query := `UPDATE activity_reports
	SET invoice_id = 0, name = ?, date = ?, hours_amount = ?
	WHERE id == ?`

	// Prepare the query
	statement, err := database.DB.Prepare(query)
	if err != nil {
		return err
	}

	// Close the statement when the function call ends
	defer statement.Close()

	// Execute the query
	_, err = statement.Exec(ar.Name, ar.Date, ar.HoursAmount, ar.ID)
	return err
}

// Function to get the list of contracts, return a list of contracts and error type
// This is not required to be a method since we don't really use the struct to insert data, we just create a list of contracts
func GetArList(userId int64, clientId int64, contractId int64, woId int64) ([]ActivityReport, error) {
	// Build the query
	query := "SELECT * FROM activity_reports where user_id == ? AND client_id == ? AND contract_id == ? AND wo_id == ?"

	// Direclty execute the query
	rows, err := database.DB.Query(query, userId, clientId, contractId, woId)
	if err != nil {
		return nil, err
	}

	// Close the database connection when function call is done
	defer rows.Close()

	// Create the data structure for the return
	var arList []ActivityReport

	// Iterate over each row
	for rows.Next() {
		// Scan each row and map the items to client properties
		// The order of the arguments for the Scan function must be the same as the DB table not the model
		var ar ActivityReport
		err := rows.Scan(&ar.ID,
			&ar.UserID,
			&ar.ClientID,
			&ar.ContractID,
			&ar.WorkOrderID,
			&ar.InvoiceId,
			&ar.Name,
			&ar.Date,
			&ar.HoursAmount)
		if err != nil {
			return nil, err
		}

		// append each client to the list of clients
		arList = append(arList, ar)
	}

	// Return the clients and no error
	return arList, nil
}

// Function to retrieve the client with a specific ID
// This is not required to be a method since we don't really use the struct to insert data, we just retrieve a client from DB
func GetArById(id int64) (*ActivityReport, error) {
	// We build the query this way to avoid SQL injection
	query := "SELECT * FROM activity_reports WHERE id == ?"
	row := database.DB.QueryRow(query, id)

	// Scan the row and map the items to client properties
	var ar ActivityReport
	err := row.Scan(&ar.ID,
		&ar.UserID,
		&ar.ClientID,
		&ar.ContractID,
		&ar.WorkOrderID,
		&ar.InvoiceId,
		&ar.Name,
		&ar.Date,
		&ar.HoursAmount)
	if err != nil {
		return nil, err
	}

	// Return the client
	return &ar, nil
}

// Method to delete a contract
func (ar ActivityReport) Delete(id int64) error {
	// Query statement
	query := "DELETE FROM activity_report WHERE id == ?"
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
