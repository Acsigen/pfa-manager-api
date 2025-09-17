package routes

import (
	"net/http"
	"strconv"

	"github.com/Acsigen/pfa-manager-api/models"
	"github.com/gin-gonic/gin"
)

func add_contract(context *gin.Context) {
	var contract models.Contract

	client_id, err := strconv.ParseInt(context.Param("id"), 10, 64)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid client ID"})
		return
	}
	err = context.ShouldBindJSON(&contract)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse request data"})
		return
	}

	contract.UserID = context.GetInt64("userId")
	contract.ClientID = client_id

	err = contract.Add()

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not add contracts"})
		return
	}

	context.JSON(http.StatusCreated, gin.H{"message": "Contract created", "contract": contract})
}
