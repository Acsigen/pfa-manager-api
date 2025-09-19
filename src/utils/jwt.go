package utils

import (
	"errors"
	"os"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

// Read the secret key from env
var secretKey string = os.Getenv("PFA_SECRET_KEY")

// Generate a new JWT Token from email and user ID
func GenerateToken(email string, userId int64) (string, error) {
	// Generate a jwt token with a validity of 12 hours from now based on email and user id. The format is HS256
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"email":      email,
		"userId":     userId,
		"expiration": time.Now().Add(time.Hour * 12).Unix(),
	})

	// return the signed token
	return token.SignedString([]byte(secretKey))
}

// Check if the token is valid
func ValidateToken(token string) (int64, error) {
	// Parse the token
	// One of the parameters of the jwt.Parse function is an anonymous function (in place function) that checks if the token was signed with HMAC method and returns the secret key
	parsedToken, err := jwt.Parse(token, func(token *jwt.Token) (any, error) {
		// Check if token is singed with HMAC method
		_, ok := token.Method.(*jwt.SigningMethodHMAC)

		// Return an error if not
		if !ok {
			return nil, errors.New("unexpected signing method")
		}

		// Return the secret key as a byte slice if ok
		return []byte(secretKey), nil
	})

	// return error if token could not be parsed
	if err != nil {
		return 0, errors.New("could not parse token")
	}

	// store the validity status of the token inside a variable
	tokenValid := parsedToken.Valid

	// If token is not valid, return an error
	if !tokenValid {
		return 0, errors.New("token is not valid")
	}

	// if token is valid, store the claims of the token
	claims, ok := parsedToken.Claims.(jwt.MapClaims)

	// if claims are not ok, return an error
	if !ok {
		return 0, errors.New("invalid token claims")
	}

	// retrieve the user ID from the claims
	// email := claims["email"].(string)
	userId := int64(claims["userId"].(float64))

	// return the user ID
	return userId, nil

}
