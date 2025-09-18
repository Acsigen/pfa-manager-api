package routes

import (
	"net/http"

	"github.com/Acsigen/pfa-manager-api/models"
	"github.com/Acsigen/pfa-manager-api/utils"
	"github.com/gin-gonic/gin"
)

// Signup function
func signup(context *gin.Context) {
	// Initialise the user model
	var user models.User

	// Check fi the JSON body matches the model
	err := context.ShouldBindJSON(&user)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse request data"})
		return
	}

	// Register the user
	err = user.Register()

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not register user."})
		return
	}

	// Hide the password from the response
	user.Password = "REDACTED"

	// Display the confirmation and user details
	context.JSON(http.StatusCreated, gin.H{"message": "User registered", "client": user})
}

// Login function
func login(context *gin.Context) {
	// initialise the skimmed model for login
	var user models.UserLogin

	// Check fi the JSON body matches the model
	err := context.ShouldBindJSON(&user)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse request data"})
		return
	}

	// Check if credentials are good
	err = user.ValidateCredentials()

	if err != nil {
		context.JSON(http.StatusUnauthorized, gin.H{"message": err.Error()})
		return
	}

	// Generate the jwt token
	jwtToken, err := utils.GenerateToken(user.EmailAddress, user.ID)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": err.Error()})
		return
	}

	// Display a message and the JWT token
	context.JSON(http.StatusOK, gin.H{"message": "Login OK", "token": jwtToken})
}
