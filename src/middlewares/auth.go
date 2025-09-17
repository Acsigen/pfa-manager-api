package middlewares

import (
	"net/http"

	"github.com/Acsigen/pfa-manager-api/utils"
	"github.com/gin-gonic/gin"
)

func Authenticate(context *gin.Context) {
	token := context.Request.Header.Get("Authorization")

	if token == "" {
		context.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"message": "Please login before performing this action"})
		return
	}

	userId, err := utils.ValidateToken(token)

	if err != nil {
		context.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"message": "Please login before performing this action"})
		return
	}

	context.Set("userId", userId)
	context.Next()
}
