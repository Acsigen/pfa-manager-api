package models

import (
	"github.com/Acsigen/pfa-manager-api/database"
)

// Client model, used tags to set the required items
type Client struct {
	Address        string `binding:"required"`
	Contact_person string `binding:"required"`
	Country        string `binding:"required"`
	CUI            string `binding:"required"`
	ID             int64
	Name           string `binding:"required"`
	ONRC_no        string `binding:"required"`
	Phone_number   string
	UserID         int64
}

// Add a new client
func (c *Client) Add() error {
	// Build the query, use ? to avoid SQL injection
	query := `INSERT INTO clients(name, address, contact_person, country, phone_number, onrc_no, cui, user_id)
	VALUES (?,?,?,?,?,?,?,?)`

	// Prepare the query
	statement, err := database.DB.Prepare(query)
	if err != nil {
		return err
	}

	// Close the statement when the function call ends
	defer statement.Close()

	// Execute the query
	res, err := statement.Exec(c.Name, c.Address, c.Contact_person, c.Country, c.Phone_number, c.ONRC_no, c.CUI, c.UserID)
	if err != nil {
		return err
	}

	// Get the last insterted ID
	id, err := res.LastInsertId()

	// Set the ID of the client object so we can return it with the object in another function
	c.ID = id
	return err
}

// Add a new client
func (c Client) Update() error {
	// Build the query, use ? to avoid SQL injection
	query := `UPDATE clients
	SET name = ?, address = ?, contact_person = ?, country = ?, phone_number = ?, onrc_no = ?, cui = ?, user_id = ?
	WHERE id = ?`

	// Prepare the query
	statement, err := database.DB.Prepare(query)
	if err != nil {
		return err
	}

	// Close the statement when the function call ends
	defer statement.Close()

	// Execute the query
	_, err = statement.Exec(c.Name, c.Address, c.Contact_person, c.Country, c.Phone_number, c.ONRC_no, c.CUI, c.UserID, c.ID)
	return err
}

// Get the list of clients, return a list of clients and error type
func Get_client_list() ([]Client, error) {
	// Build the query
	query := "SELECT * FROM clients"

	// Direclty execute the query
	rows, err := database.DB.Query(query)
	if err != nil {
		return nil, err
	}

	// Close the database connection when function call is done
	defer rows.Close()

	// Create the data structure for the return
	var clients []Client

	// Iterate over each row
	for rows.Next() {
		// Scan each row and map the items to client properties
		var client Client
		err := rows.Scan(&client.ID,
			&client.Name,
			&client.Address,
			&client.Contact_person,
			&client.Country,
			&client.Phone_number,
			&client.ONRC_no,
			&client.CUI,
			&client.UserID)
		if err != nil {
			return nil, err
		}

		// append each client to the list of clients
		clients = append(clients, client)
	}

	// Return the clients and no error
	return clients, nil
}

// Retrieve the client with a specific ID
func GetEventById(id int64) (*Client, error) {
	// We build the query this way to avoid SQL injection
	query := "SELECT * FROM clients WHERE id == ?"
	row := database.DB.QueryRow(query, id)

	var client Client
	err := row.Scan(&client.ID,
		&client.Name,
		&client.Address,
		&client.Contact_person,
		&client.Country,
		&client.Phone_number,
		&client.ONRC_no,
		&client.CUI,
		&client.UserID)
	if err != nil {
		return nil, err
	}

	return &client, nil
}

func (c Client) Delete(id int64) error {
	query := "DELETE FROM clients WHERE id == ?"
	statement, err := database.DB.Prepare(query)
	if err != nil {
		return err
	}

	defer statement.Close()

	_, err = statement.Exec(id)

	return err
}
