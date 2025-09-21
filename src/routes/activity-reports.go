package routes

import (
	"net/http"
	"strconv"

	"github.com/Acsigen/pfa-manager-api/models"
	"github.com/Acsigen/pfa-manager-api/utils"
	"github.com/gin-gonic/gin"
)

// Display the list
func get_ar_list(context *gin.Context) {
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

	// Get the client id from path
	woPathId, err := strconv.ParseInt(context.Param("wo_id"), 10, 64)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid work order ID"})
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
	arList, err := models.GetArList(userId, clientPathId, contractPathId, woPathId)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch activity reports."})
		return
	}

	// Return the clients if everything is ok
	context.JSON(http.StatusOK, arList)
}

// Add a new contract function
func add_ar(context *gin.Context) {
	// Initialise the model
	var ar models.ActivityReport

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

	wo_id, err := strconv.ParseInt(context.Param("wo_id"), 10, 64)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid work order ID"})
		return
	}

	// Check if the JSON body matches the model
	err = context.ShouldBindJSON(&ar)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse request data"})
		return
	}

	// Get the User ID from the context
	ar.UserID = context.GetInt64("userId")

	// Set the proper client ID
	ar.ClientID = client_id

	ar.ContractID = contract_id

	ar.WorkOrderID = wo_id

	// TODO: Implement proper invoice ID once the invoice section is done
	ar.InvoiceId = 0

	// Get the client based on ID from path parameter
	client, err := models.GetClientById(client_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch client for permission check"})
		return
	}

	// Only the owner can update data
	err = utils.CheckPermissions(ar.UserID, client.UserID)

	if err != nil {
		context.JSON(http.StatusUnauthorized, gin.H{"message": err.Error()})
		return
	}

	// Add the wo to DB
	err = ar.Add()

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not add activity report"})
		return
	}

	// Display confirmation message and contract contents
	context.JSON(http.StatusCreated, gin.H{"message": "Work order created", "activity_report": ar})
}

func get_ar(context *gin.Context) {
	// Retrieve the path parameter
	_, err := strconv.ParseInt(context.Param("wo_id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid work order ID"})
		return
	}

	ar_id, err := strconv.ParseInt(context.Param("ar_id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid activity report ID"})
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
	ar, err := models.GetArById(ar_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch activity report.", "error": err.Error()})
		return
	}

	// Only the owner can update data
	err = utils.CheckPermissions(userId, ar.UserID)
	if err != nil {
		context.JSON(http.StatusUnauthorized, gin.H{"message": err.Error()})
		return
	}

	// Display the contract details with proper response code
	context.JSON(http.StatusOK, ar)
}

func update_ar(context *gin.Context) {
	// Retrieve the path parameter
	client_id, err := strconv.ParseInt(context.Param("id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid client ID"})
		return
	}

	ar_id, err := strconv.ParseInt(context.Param("ar_id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid activity report ID"})
		return
	}

	_, err = strconv.ParseInt(context.Param("wo_id"), 10, 64)
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
	var updatedAr models.ActivityReport
	err = context.ShouldBindJSON(&updatedAr)

	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Could not parse activity report data."})
	}

	// Set the proper contract ID
	updatedAr.ID = ar_id

	// Update the contract
	err = updatedAr.Update()
	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not update activity report."})
		return
	}

	// Display a confirmation
	context.JSON(http.StatusOK, gin.H{"message": "Activity report updated updated"})
}

func delete_ar(context *gin.Context) {
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

	_, err = strconv.ParseInt(context.Param("wo_id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid work order ID"})
		return
	}

	ar_id, err := strconv.ParseInt(context.Param("ar_id"), 10, 64)
	if err != nil {
		context.JSON(http.StatusBadRequest, gin.H{"message": "Invalid activity report ID"})
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

	ar, err := models.GetArById(ar_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not fetch activity repory for deletion."})
		return
	}

	// Delete the client
	err = ar.Delete(ar_id)

	if err != nil {
		context.JSON(http.StatusInternalServerError, gin.H{"message": "Could not delete activity report."})
		return
	}

	// Display confirmation
	context.JSON(http.StatusOK, gin.H{"message": "Activity report deleted."})

}
