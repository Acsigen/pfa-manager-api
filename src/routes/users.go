package routes

import (
	"net/http"

	"github.com/Acsigen/pfa-manager-api/models"
	"github.com/Acsigen/pfa-manager-api/utils"
	"github.com/gin-gonic/gin"
)

func signup(context *gin.Context) {
	var user models.User

	err := context.ShouldBindJSON(&user)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse request data"})
		return
	}

	err = user.Register()

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not register user."})
		return
	}

	user.Password = "REDACTED"
	context.JSON(http.StatusCreated, gin.H{"message": "User registered", "client": user})
}

func login(context *gin.Context) {
	var user models.UserLogin

	err := context.ShouldBindJSON(&user)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse request data"})
		return
	}

	err = user.ValidateCredentials()

	if err != nil {
		context.JSON(http.StatusUnauthorized, gin.H{"message": err.Error()})
		return
	}

	jwtToken, err := utils.GenerateToken(user.EmailAddress, user.ID)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": err.Error()})
		return
	}

	context.JSON(http.StatusOK, gin.H{"message": "Login OK", "token": jwtToken})
}
