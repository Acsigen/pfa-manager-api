package models

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

// // Add a new contract
// func (w *WorkOrder) Add() error {
// 	// Build the query, use ? to avoid SQL injection
// 	query := `INSERT INTO work_orders(user_id, client_id, contract_id, name, final_client, client_project_code, start_date, end_date, price, currency, measurement_unit, status)
// 	VALUES (?,?,?,?,?,?,?,?,?,?,?,?)`

// 	// Prepare the query
// 	statement, err := database.DB.Prepare(query)
// 	if err != nil {
// 		return err
// 	}

// 	// Close the statement when the function call ends
// 	defer statement.Close()

// 	// Execute the query
// 	res, err := statement.Exec(w.UserID, w.ClientID, w.ContractID, w.Name, w.FinalClient, w.ClientProjectCode, w.StartDate, w.EndDate, w.Price, w.Currency, w.MeasurementUnit, w.Status)
// 	if err != nil {
// 		return err
// 	}

// 	// Get the last insterted ID
// 	id, err := res.LastInsertId()

// 	// Set the ID of the client object so we can return it with the object in another function
// 	w.ID = id
// 	return err
// }

// // Method for updating a contract
// func (w *WorkOrder) Update() error {
// 	// Build the query, use ? to avoid SQL injection
// 	query := `UPDATE work_orders
// 	SET name = ?, final_client = ?, client_project_code = ?, start_date = ?, end_date = ?, price = ?, currency = ?, measurement_unit = ?, status = ?
// 	WHERE id == ?`

// 	// Prepare the query
// 	statement, err := database.DB.Prepare(query)
// 	if err != nil {
// 		return err
// 	}

// 	// Close the statement when the function call ends
// 	defer statement.Close()

// 	// Execute the query
// 	_, err = statement.Exec(w.Name, w.FinalClient, w.ClientProjectCode, w.StartDate, w.EndDate, w.Price, w.Currency, w.MeasurementUnit, w.Status, w.ID)
// 	return err
// }

// // Function to get the list of contracts, return a list of contracts and error type
// // This is not required to be a method since we don't really use the struct to insert data, we just create a list of contracts
// func GetWoList(userId int64, clientId int64, contractId int64) ([]WorkOrder, error) {
// 	// Build the query
// 	query := "SELECT * FROM work_orders where user_id == ? AND client_id == ? AND contract_id == ?"

// 	// Direclty execute the query
// 	rows, err := database.DB.Query(query, userId, clientId, contractId)
// 	if err != nil {
// 		return nil, err
// 	}

// 	// Close the database connection when function call is done
// 	defer rows.Close()

// 	// Create the data structure for the return
// 	var woList []WorkOrder

// 	// Iterate over each row
// 	for rows.Next() {
// 		// Scan each row and map the items to client properties
// 		// The order of the arguments for the Scan function must be the same as the DB table not the model
// 		var wo WorkOrder
// 		err := rows.Scan(&wo.ID,
// 			&wo.UserID,
// 			&wo.ClientID,
// 			&wo.ContractID,
// 			&wo.Name,
// 			&wo.FinalClient,
// 			&wo.ClientProjectCode,
// 			&wo.StartDate,
// 			&wo.EndDate,
// 			&wo.Price,
// 			&wo.Currency,
// 			&wo.MeasurementUnit,
// 			&wo.Status)
// 		if err != nil {
// 			return nil, err
// 		}

// 		// append each client to the list of clients
// 		woList = append(woList, wo)
// 	}

// 	// Return the clients and no error
// 	return woList, nil
// }

// // Function to retrieve the client with a specific ID
// // This is not required to be a method since we don't really use the struct to insert data, we just retrieve a client from DB
// func GetWoById(id int64) (*WorkOrder, error) {
// 	// We build the query this way to avoid SQL injection
// 	query := "SELECT * FROM work_orders WHERE id == ?"
// 	row := database.DB.QueryRow(query, id)

// 	// Scan the row and map the items to client properties
// 	var wo WorkOrder
// 	err := row.Scan(&wo.ID,
// 		&wo.UserID,
// 		&wo.ClientID,
// 		&wo.ContractID,
// 		&wo.Name,
// 		&wo.FinalClient,
// 		&wo.ClientProjectCode,
// 		&wo.StartDate,
// 		&wo.EndDate,
// 		&wo.Price,
// 		&wo.Currency,
// 		&wo.MeasurementUnit,
// 		&wo.Status)
// 	if err != nil {
// 		return nil, err
// 	}

// 	// Return the client
// 	return &wo, nil
// }

// // Method to delete a contract
// func (w WorkOrder) Delete(id int64) error {
// 	// Query statement
// 	query := "DELETE FROM work_orders WHERE id == ?"
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
