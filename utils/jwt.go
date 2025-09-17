package utils

import (
	"time"

	"github.com/golang-jwt/jwt/v5"
)

// TODO: Get from environment
const secretKey = "supersecret"

func GenerateToken(email string, userId int64) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"email":      email,
		"userId":     userId,
		"expiration": time.Now().Add(time.Hour * 12).Unix(),
	})

	return token.SignedString([]byte(secretKey))
}
