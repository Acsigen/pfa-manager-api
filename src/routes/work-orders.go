package routes

import (
	"net/http"
	"strconv"

	"github.com/Acsigen/pfa-manager-api/models"
	"github.com/Acsigen/pfa-manager-api/utils"
	"github.com/gin-gonic/gin"
)

// Display the list
func get_wo_list(context *gin.Context) {
	// Get the user id from the authentication middleware
	userId := context.GetInt64("userId")

	// Get the client id from path
	clientPathId, err := strconv.ParseInt(context.Param("id"), 10, 64)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid client ID"})
		return
	}

	// Get the client id from path
	contractPathId, err := strconv.ParseInt(context.Param("contract_id"), 10, 64)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid contract ID"})
		return
	}

	// Get the client data
	client, err := models.GetClientById(clientPathId)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch client for permissions check"})
		return
	}

	// check permissions
	err = utils.CheckPermissions(userId, client.ID)

	if err != nil {
		context.JSON(http.StatusUnauthorized, gin.H{"message": err.Error()})
		return
	}

	// Get the list
	woList, err := models.GetWoList(userId, clientPathId, contractPathId)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch work orders."})
		return
	}

	// Return the clients if everything is ok
	context.JSON(http.StatusOK, woList)
}

// Add a new contract function
func add_wo(context *gin.Context) {
	// Initialise the model
	var wo models.WorkOrder

	// Get the client ID from the path parameter
	client_id, err := strconv.ParseInt(context.Param("id"), 10, 64)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid client ID"})
		return
	}

	contract_id, err := strconv.ParseInt(context.Param("contract_id"), 10, 64)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid contract ID"})
		return
	}

	// Check if the JSON body matches the model
	err = context.ShouldBindJSON(&wo)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse request data"})
		return
	}

	// Get the User ID from the context
	wo.UserID = context.GetInt64("userId")

	// Set the proper client ID
	wo.ClientID = client_id

	wo.ContractID = contract_id

	// Get the client based on ID from path parameter
	client, err := models.GetClientById(client_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch client for permission check"})
		return
	}

	// Only the owner can update data
	err = utils.CheckPermissions(wo.UserID, client.UserID)

	if err != nil {
		context.JSON(http.StatusUnauthorized, gin.H{"message": err.Error()})
		return
	}

	// Add the wo to DB
	err = wo.Add()

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not add work order"})
		return
	}

	// Display confirmation message and contract contents
	context.JSON(http.StatusCreated, gin.H{"message": "Work order created", "contract": wo})
}

func get_wo(context *gin.Context) {
	// Retrieve the path parameter
	wo_id, err := strconv.ParseInt(context.Param("wo_id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid work order ID"})
		return
	}

	_, err = strconv.ParseInt(context.Param("contract_id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid contract ID"})
		return
	}

	_, err = strconv.ParseInt(context.Param("id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid client ID"})
		return
	}

	// Get the user id from the authentication middleware
	userId := context.GetInt64("userId")

	// Get the contract details from DB
	wo, err := models.GetWoById(wo_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch wokr order.", "error": err.Error()})
		return
	}

	// Only the owner can update data
	err = utils.CheckPermissions(userId, wo.UserID)
	if err != nil {
		context.JSON(http.StatusUnauthorized, gin.H{"message": err.Error()})
		return
	}

	// Display the contract details with proper response code
	context.JSON(http.StatusOK, wo)
}

func update_wo(context *gin.Context) {
	// Retrieve the path parameter
	client_id, err := strconv.ParseInt(context.Param("id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid client ID"})
		return
	}

	wo_id, err := strconv.ParseInt(context.Param("wo_id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid work order ID"})
		return
	}

	// Get the user id from the authentication middleware
	userId := context.GetInt64("userId")

	// Get the client based on ID from path parameter
	client, err := models.GetClientById(client_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch client for permission check"})
		return
	}

	// Only the owner can update data
	err = utils.CheckPermissions(userId, client.UserID)
	if err != nil {
		context.JSON(http.StatusUnauthorized, gin.H{"message": err.Error()})
		return
	}

	// Initialise the updated client that should match the model
	var updatedWo models.WorkOrder
	err = context.ShouldBindJSON(&updatedWo)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse work order data."})
	}

	// Set the proper contract ID
	updatedWo.ID = wo_id

	// Update the contract
	err = updatedWo.Update()
	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not update work order."})
		return
	}

	// Display a confirmation
	context.JSON(http.StatusOK, gin.H{"message": "Work order updated"})
}

func delete_wo(context *gin.Context) {
	// Retrieve the path parameter
	client_id, err := strconv.ParseInt(context.Param("id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid client ID"})
		return
	}

	_, err = strconv.ParseInt(context.Param("contract_id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid contract ID"})
		return
	}

	wo_id, err := strconv.ParseInt(context.Param("wo_id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid work order ID"})
		return
	}

	// Get the user id from the authentication middleware
	userId := context.GetInt64("userId")

	// Get the client based on ID from path parameter
	client, err := models.GetClientById(client_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch client for permission check."})
		return
	}

	// Only the owner can update data
	err = utils.CheckPermissions(userId, client.UserID)
	if err != nil {
		context.JSON(http.StatusUnauthorized, gin.H{"message": err.Error()})
		return
	}

	wo, err := models.GetWoById(wo_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch work order for deletion."})
		return
	}

	// Delete the client
	err = wo.Delete(wo_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not delete work order."})
		return
	}

	// Display confirmation
	context.JSON(http.StatusOK, gin.H{"message": "Work order deleted."})

}
