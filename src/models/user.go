package models

import (
	"errors"

	"github.com/Acsigen/pfa-manager-api/database"
	"github.com/Acsigen/pfa-manager-api/utils"
)

// User model
type User struct {
	ID           int64
	FirstName    string `binding:"required"`
	LastName     string `binding:"required"`
	PhoneNumber  string `binding:"required"`
	EmailAddress string `binding:"required"`
	Password     string `binding:"required"`
}

// Another user model used for login procedure
// We do not want to place all  other items in the login form. We want them mandatory only for the DB insert
type UserLogin struct {
	ID           int64
	EmailAddress string `binding:"required"`
	Password     string `binding:"required"`
}

// User registration
func (u *User) Register() error {
	// query preparation
	query := "INSERT INTO users(first_name, last_name, phone_number, email_address, password) VALUES (?, ?, ?, ?, ?)"

	statement, err := database.DB.Prepare(query)
	if err != nil {
		return err
	}

	// Close the statement when the function call ends
	defer statement.Close()

	// retrieve the hash of the password to be stored inside the DB
	hashed_pass, err := utils.HashPassword(u.Password)
	if err != nil {
		return err
	}

	// Execute the query
	res, err := statement.Exec(u.FirstName, u.LastName, u.PhoneNumber, u.EmailAddress, hashed_pass)
	if err != nil {
		return err
	}

	// Get the last insterted ID
	id, err := res.LastInsertId()

	// Set the ID of the client object to match the one in the DB so we can use it with the object in another function
	u.ID = id

	return err

}

// Login procedure
func (u *UserLogin) ValidateCredentials() error {
	// prepare the query
	query := "SELECT id,password FROM users where email_address = ?"

	// Since is just one row, we execute it directly
	row := database.DB.QueryRow(query, u.EmailAddress)

	// get the User ID and the Hashed password
	var retrievedPassword string
	err := row.Scan(&u.ID, &retrievedPassword)

	if err != nil {
		return errors.New("invalid credentials")
	}

	// Check if the hash of the password inside the DB matches the hash of the input password
	isValidPassword := utils.CheckHash(u.Password, retrievedPassword)

	if !isValidPassword {
		return errors.New("invalid credentials")
	}

	// return nothing if all good
	return nil
}
