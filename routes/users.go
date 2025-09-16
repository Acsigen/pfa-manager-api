package routes

import (
	"fmt"
	"net/http"

	"github.com/Acsigen/pfa-manager-api/models"
	"github.com/gin-gonic/gin"
)

func signup(context *gin.Context) {
	var user models.User

	err := context.ShouldBindJSON(&user)

	fmt.Println(err)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse request data"})
		return
	}

	err = user.Register()

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not register user."})
		return
	}

	context.JSON(http.StatusCreated, gin.H{"message": "User registered", "client": user})
}
