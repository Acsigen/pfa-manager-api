package utils

import "golang.org/x/crypto/bcrypt"

// Hash a password to be stored in a DB
func HashPassword(password string) (string, error) {
	hashed_pass, err := bcrypt.GenerateFromPassword([]byte(password), 16)
	return string(hashed_pass), err
}

// check if the hash matches current password used by the user
func CheckHash(password string, hashedPassword string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hashedPassword), []byte(password))
	return err == nil
}
