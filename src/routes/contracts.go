package routes

import (
	"net/http"
	"strconv"

	"github.com/Acsigen/pfa-manager-api/models"
	"github.com/gin-gonic/gin"
)

// Add a new contract function
func add_contract(context *gin.Context) {
	// Initialise the model
	var contract models.Contract

	// Get the client ID from the path parameter
	client_id, err := strconv.ParseInt(context.Param("id"), 10, 64)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid client ID"})
		return
	}

	// Check if the JSON body matches the model
	err = context.ShouldBindJSON(&contract)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse request data"})
		return
	}

	// Get the User ID from the context
	contract.UserID = context.GetInt64("userId")

	// Set the proper client ID
	contract.ClientID = client_id

	// Add the contract to DB
	err = contract.Add()

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not add contracts"})
		return
	}

	// Display confirmation message and contract contents
	context.JSON(http.StatusCreated, gin.H{"message": "Contract created", "contract": contract})
}
