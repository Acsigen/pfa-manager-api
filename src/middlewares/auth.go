package middlewares

import (
	"net/http"

	"github.com/Acsigen/pfa-manager-api/utils"
	"github.com/gin-gonic/gin"
)

// Authentication middleware
func Authenticate(context *gin.Context) {

	// Get the token from the request header
	token := context.Request.Header.Get("Authorization")

	// If token is missing, return message
	if token == "" {
		context.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"message": "Please login before performing this action"})
		return
	}

	// Check if token is valid
	userId, err := utils.ValidateToken(token)

	// If not valid, return message
	if err != nil {
		context.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"message": "Please login before performing this action"})
		return
	}

	// If valid, set the user ID from the token specs
	context.Set("userId", userId)

	// Continue with the next step of the request. Since this is a middleware, it gets executed before the request reaches the actual endpoint
	context.Next()
}
