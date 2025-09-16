package models

import (
	"github.com/Acsigen/pfa-manager-api/database"
)

type User struct {
	ID           int64
	FirstName    string `binding:"required"`
	LastName     string `binding:"required"`
	PhoneNumber  string `binding:"required"`
	EmailAddress string `binding:"required"`
	Password     string `binding:"required"`
}

func (u User) Register() error {
	query := "INSERT INTO users(first_name, last_name, phone_number, email_address, password) VALUES (?, ?, ?, ?, ?)"

	statement, err := database.DB.Prepare(query)
	if err != nil {
		return err
	}

	// Close the statement when the function call ends
	defer statement.Close()

	// Execute the query
	res, err := statement.Exec(u.FirstName, u.LastName, u.PhoneNumber, u.EmailAddress, u.Password)
	if err != nil {
		return err
	}

	// Get the last insterted ID
	id, err := res.LastInsertId()

	// Set the ID of the client object so we can return it with the object in another function
	u.ID = id
	return err

}
